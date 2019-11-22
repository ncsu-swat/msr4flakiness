package com.outbrain.aletheia;

import com.outbrain.aletheia.breadcrumbs.AggregatingBreadcrumbDispatcher;
import com.outbrain.aletheia.breadcrumbs.Breadcrumb;
import com.outbrain.aletheia.breadcrumbs.BreadcrumbDispatcher;
import com.outbrain.aletheia.breadcrumbs.BreadcrumbHandler;
import com.outbrain.aletheia.breadcrumbs.BreadcrumbKey;
import com.outbrain.aletheia.breadcrumbs.KeyedBreadcrumbBaker;
import com.outbrain.aletheia.breadcrumbs.KeyedBreadcrumbDispatcher;
import com.outbrain.aletheia.breadcrumbs.StartTimeWithDurationBreadcrumbBaker;
import com.outbrain.aletheia.datum.DatumUtils;
import com.outbrain.aletheia.datum.PeriodicBreadcrumbDispatcher;

import org.joda.time.Duration;
import org.joda.time.Instant;
import org.joda.time.Interval;
import org.junit.Ignore;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.TestName;

import java.io.PrintWriter;
import java.util.LinkedList;
import java.util.List;
import java.util.Random;
import java.util.UUID;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicLong;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

import static org.hamcrest.core.Is.is;
import static org.junit.Assert.assertThat;

/**
 * Created by slevin on 8/28/14.
 */
@Ignore
public class DatumAuditorStressTest {

  @Rule
  public final TestName testName = new TestName();

  private static final String TEST_RESULT_FILE_NAME = "/tmp/breadcrumb_%s.txt";
  private static final int THREAD_COUNT = 500;
  private static final int NUM_UNIQUE_PRODUCERS = 4000;

  private final Random random = new Random();
  private final ScheduledExecutorService scheduledExecutorService = Executors.newSingleThreadScheduledExecutor();
  private final AtomicLong hitCount = new AtomicLong(0);
  private final Duration bucketDuration = Duration.standardSeconds(10);
  private final Duration durationBetweenFlushes = Duration.standardSeconds(30);
  private final Duration testDuration = Duration.standardHours(1);

  private final BreadcrumbHandler hitCountUpdater = new BreadcrumbHandler() {
    @Override
    public void handle(final Breadcrumb breadcrumb) {
      hitCount.getAndAdd(breadcrumb.getCount());
    }

    @Override
    public void close() throws Exception {

    }
  };

  private void doBenchmark(final BreadcrumbDispatcher<SampleDomainClass> breadcrumbDispatcher) throws Exception {

    final List<String> idList = IntStream.range(0, NUM_UNIQUE_PRODUCERS)
                                         .mapToObj(__ -> UUID.randomUUID().toString())
                                         .collect(Collectors.toList());

    final Instant start = Instant.now();
    final AtomicLong[] hitReportCounts = new AtomicLong[THREAD_COUNT];

    final ExecutorService executorService = Executors.newFixedThreadPool(THREAD_COUNT);
    final LinkedList<Future<?>> submits = new LinkedList<>();

    for (int j = 0; j < THREAD_COUNT; j++) {
      final AtomicLong atomicLong = new AtomicLong(0);
      hitReportCounts[j] = atomicLong;
      submits.add(executorService.submit(new Runnable() {
        public void run() {
          final Instant end = Instant.now().plus(testDuration);
          while (Instant.now().isBefore(end)) {
            breadcrumbDispatcher.report(new SampleDomainClass(1, 1, idList.get(random.nextInt(idList.size())), Instant.now(), true));
            atomicLong.incrementAndGet();
          }
        }
      }));
    }

    for (final Future<?> submit : submits) {
      submit.get();
    }

    // some extra waiting to make sure we have flushed it all
    executorService.awaitTermination(durationBetweenFlushes.getStandardSeconds() * 2, TimeUnit.SECONDS);

    final PrintWriter writer = new PrintWriter(String.format(TEST_RESULT_FILE_NAME, testName.getMethodName()),
        "UTF-8");

    writer.println(String.format("Test time in millis: %d", new Interval(start, Instant.now()).toDurationMillis()));

    long totalHitReportCount = 0;

    for (int j = 0; j < THREAD_COUNT; j++) {
      writer.println(String.format("Thread [%d] got [%d] incoming hits", j, hitReportCounts[j].get()));
      totalHitReportCount += hitReportCounts[j].get();
    }

    writer.println(String.format("Total incoming hits: %d, Total outgoing hits: %d, status: %B",
        totalHitReportCount,
        hitCount.get(),
        totalHitReportCount == hitCount.get()));
    writer.close();

    assertThat(hitCount.get(), is(totalHitReportCount));
  }

  @Test
  public void test_breadcrumbDispatcher_under_load() throws Exception {

    final BreadcrumbDispatcher<SampleDomainClass> aggregatingDispatcher = new AggregatingBreadcrumbDispatcher<>(
        bucketDuration,
        DatumUtils.getDatumTimestampExtractor(SampleDomainClass.class),
        new StartTimeWithDurationBreadcrumbBaker("", "", "", "", "", ""),
        hitCountUpdater,
        Duration.standardDays(1));

    doBenchmark(
        new PeriodicBreadcrumbDispatcher<>(aggregatingDispatcher,
            scheduledExecutorService,
            durationBetweenFlushes)
    );
  }

  @Test
  public void test_keyedBreadcrumbDispatcher_under_load() throws Exception {
    final BreadcrumbDispatcher<SampleDomainClass> keyedDispatcher = new KeyedBreadcrumbDispatcher<>(
        bucketDuration,
        DatumUtils.getDatumTimestampExtractor(SampleDomainClass.class),
        new KeyedBreadcrumbBaker("", ""),
        hitCountUpdater,
        datum -> new BreadcrumbKey("", datum.getMyString(), "", ""),
        Duration.standardDays(1));

    doBenchmark(
        new PeriodicBreadcrumbDispatcher<>(keyedDispatcher,
            scheduledExecutorService,
            durationBetweenFlushes)
    );
  }
}
