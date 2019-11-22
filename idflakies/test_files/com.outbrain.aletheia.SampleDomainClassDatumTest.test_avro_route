package com.outbrain.aletheia;

import com.google.common.base.Predicate;
import com.outbrain.aletheia.configuration.routing.Route;
import org.apache.commons.lang3.RandomStringUtils;
import org.joda.time.Instant;
import org.junit.Test;

/**
 * Created by slevin on 8/16/14.
 */
public class SampleDomainClassDatumTest extends AletheiaIntegrationTest<SampleDomainClass> {

  public static final Route AVRO_ROUTE = new Route("test_endpoint_1", "avro");
  public static final Route JSON_ROUTE = new Route("test_endpoint_2", "json");

  private final Predicate<SampleDomainClass> filter = new Predicate<SampleDomainClass>() {
    @Override
    public boolean apply(final SampleDomainClass input) {
      return input.isDiscarded();
    }
  };

  public SampleDomainClassDatumTest() {
    super(SampleDomainClass.class);
  }

  @Override
  protected SampleDomainClass domainClassRandomDatum(final boolean shouldBeSent) {
    return new SampleDomainClass(random.nextInt(),
                                 random.nextDouble(),
                                 RandomStringUtils.randomAlphanumeric(random.nextInt(20)),
                                 new Instant(),
                                 shouldBeSent);
  }

  @Test
  public void test_avro_route() throws InterruptedException {
    testRoutes(AVRO_ROUTE);
  }

  @Test
  public void test_json_route() throws InterruptedException {
    testRoutes(JSON_ROUTE);
  }

  @Test
  public void test_multiple_routes() throws InterruptedException {
    testRoutes(AVRO_ROUTE, JSON_ROUTE);
  }
}
