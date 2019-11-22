package com.spinn3r.noxy.discovery.zookeeper;

import com.google.common.base.Stopwatch;
import com.google.common.collect.Lists;
import com.google.common.collect.Maps;
import com.google.inject.Inject;
import com.google.inject.Provider;
import com.spinn3r.artemis.init.Launcher;
import com.spinn3r.artemis.init.ServiceReferences;
import com.spinn3r.artemis.zookeeper.embedded.EmbeddedZookeeperService;
import com.spinn3r.artemis.zookeeper.init.ZookeeperService;
import com.spinn3r.noxy.discovery.*;
import com.spinn3r.noxy.discovery.zookeeper.init.ZKDiscoveryService;
import org.apache.curator.framework.CuratorFramework;
import org.apache.zookeeper.data.Stat;
import org.junit.Before;
import org.junit.Test;

import java.util.List;
import java.util.Map;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicLong;

import static org.junit.Assert.*;

import static com.jayway.awaitility.Awaitility.*;

public class ZKTest {

    Launcher launcher;

    @Inject
    DiscoveryFactory discoveryFactory;

    @Inject
    MembershipFactory membershipFactory;

    @Inject
    Provider<CuratorFramework> curatorFrameworkProvider;

    Cluster cluster = new Cluster( "test" );

    Datacenter datacenter = new Datacenter( "local", "Castro Valley, CA" );
    Endpoint endpoint = new Endpoint( "localhost:12345", "localhost", EndpointType.WEBSERVER, datacenter );

    @Before
    public void setUp() throws Exception {

        launcher = Launcher.newBuilder().build();
        launcher.launch( new TestServiceReferences() );

        launcher.getInjector().injectMembers( this );

    }

    @Test
    public void testMembershipJoinAndLeave() throws Exception {

        Membership membership = membershipFactory.create( cluster );
        membership.join( endpoint );

        // now assert that the node is created and that it's the right paths and mode.

        String path = ZKClusterPaths.endpoint( cluster, endpoint );

        CuratorFramework curatorFramework = curatorFrameworkProvider.get();
        byte[] data = curatorFramework.getData().forPath( path );
        Endpoint endpoint0 = Endpoint.fromJSON( data );

        Stat stat = curatorFramework.checkExists().forPath( path );

        System.out.printf( "stat: %s\n", stat );
        System.out.printf( "stat (ephemeral owner): %s\n", stat.getEphemeralOwner() );
        assertTrue( stat.getEphemeralOwner() > 0 );

        assertNotNull( stat );

        assertEquals( endpoint.toString(), endpoint0.toString() );

        membership.leave( endpoint );

        stat = curatorFramework.checkExists().forPath( path );
        assertNull( stat );

    }

    @Test
    public void testDiscoveryListener() throws Exception {

        Map<String,Endpoint> endpointMap = Maps.newConcurrentMap();

        CountDownLatch joinLatch = new CountDownLatch( 1 );
        CountDownLatch leaveLatch = new CountDownLatch( 1 );

        DiscoveryListener discoveryListener = new DiscoveryListener() {

            @Override
            public void onJoin(Endpoint endpoint) {
                endpointMap.put( endpoint.getAddress(), endpoint );
                joinLatch.countDown();
            }

            @Override
            public void onLeave(Endpoint endpoint) {
                endpointMap.remove( endpoint.getAddress() );
                leaveLatch.countDown();
            }

        };

        Discovery discovery = discoveryFactory.create( cluster, discoveryListener );

        Membership membership = membershipFactory.create( cluster );
        membership.join( endpoint );

        joinLatch.await();

        System.out.printf( "Got our onJoin call\n" );

        membership.leave( endpoint );

        System.out.printf( "Left the cluster\n" );

        leaveLatch.await();

        System.out.printf( "done\n" );

    }

    @Test
    public void testBulkClusterJoining() throws Exception {

        Map<String,Endpoint> endpointMap = Maps.newConcurrentMap();

        DiscoveryListener discoveryListener = new DiscoveryListener() {

            @Override
            public void onJoin(Endpoint endpoint) {
                endpointMap.put( endpoint.getAddress(), endpoint );
            }

            @Override
            public void onLeave(Endpoint endpoint) {
                endpointMap.remove( endpoint.getAddress() );
            }

        };

        ZKDiscovery zkDiscovery = (ZKDiscovery)discoveryFactory.create( cluster, discoveryListener );

        AtomicLong onChildrenCalls = new AtomicLong( 0 );

        zkDiscovery.setZkDiscoveryStateListener( children -> onChildrenCalls.getAndIncrement() );

        Membership membership = membershipFactory.create( cluster );

        Stopwatch stopwatch = Stopwatch.createStarted();

        // setting this to 100k takes about 1.5 minutes to register them all
        int nrRecords = 10_000;

        List<Endpoint> endpoints = Lists.newArrayList();

        System.out.printf( "Joining nodes...\n" );

        for (int i = 0; i < nrRecords; i++) {

            Endpoint endpoint = new Endpoint( "localhost:" + (1000 + i), "localhost", EndpointType.WEBSERVER, datacenter );
            membership.join( endpoint );
            endpoints.add( endpoint );

        }

        System.out.printf( "Leaving nodes...\n" );

        await()
          .timeout( 60, TimeUnit.SECONDS )
          .until( () -> {
              assertEquals( nrRecords, endpointMap.size() );
          } );

        for (Endpoint endpoint : endpoints) {
            membership.leave( endpoint );
        }

        await()
          .timeout( 60, TimeUnit.SECONDS )
          .until( () -> { assertEquals( 0, endpointMap.size() ); } );

        System.out.printf( "NR getChildren calls: %s\n", onChildrenCalls.get() );

        assertTrue( onChildrenCalls.get() < 100 );

        System.out.printf( "Took: %s\n", stopwatch.stop() );

    }

    static class TestServiceReferences extends ServiceReferences {

        public TestServiceReferences() {
            add( EmbeddedZookeeperService.class );
            add( ZookeeperService.class );
            add( ZKDiscoveryService.class );
        }

    }

}