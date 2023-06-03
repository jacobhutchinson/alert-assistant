from datadog import initialize, api
from datetime import datetime
import pandas as pd
import logging


LOG = logging.getLogger(__name__)


options = {
    "api_key": API_KEY,
    "app_key": APP_KEY,
    "api_host": "https://api.datadoghq.com",
}


initialize(**options)


start = 1684454400  # Friday, May 19, 2023 12:00:00 AM
end = 1684540799  # Friday, May 19, 2023 11:59:59 PM
time_delta = 12000  # run datadog metric collection every minute (12k = 1min)


query = "avg:kubernetes.cpu.requests{kube_cluster_name:de-prd-use1-001,kube_container_name:salesforce-data-extensions} by {container_name,kube_deployment,service,kube_namespace,kube_cluster_name}"


query2 = "avg:kubernetes.cpu.requests{kube_cluster_name:de-prd-use1-001,kube_deployment:transunion-addresses-v20200924-deployment} by {container_name,kube_deployment,service,kube_namespace,kube_cluster_name}"


def extract(query, start_at, end_at, time_delta):
    LOG.info("Running extraction for cpu utilization")

    """
    datadog return data as a json blob with a field called 'series' that stores a list called 'pointlist' which has metrics like :
    * timestamp of the point for which the metric was extracted for.
    * value of the field at this timestamp.
    """

    datetime_list = []
    value_list = []
    metric_list = []

    iteration_end = start_at + time_delta

    while iteration_end <= end_at:

        results = api.Metric.query(start=start_at, end=iteration_end, query=query)
        for datadog_result in results["series"]:
            for time_value_pair_list in datadog_result["pointlist"]:
                converted_datetime = datetime.fromtimestamp(
                    time_value_pair_list[0] / 1000
                )

                datetime_list.append(converted_datetime)
                value_list.append(time_value_pair_list[1])
                metric_list.append(
                    datadog_result["metric"]
                )  # store the query that was executed in datadog.

        # increment the time spans
        start_at = iteration_end  # change start time as end of last iteration
        iteration_end = iteration_end + time_delta  # increment reading frame

        # logging logic to see extraction progress
        print(
            "finished extracting data from ",
            datetime.fromtimestamp(start_at).strftime("%c"),
            " to ",
            datetime.fromtimestamp(iteration_end).strftime("%c"),
        )

    all_data = {"datetime": datetime_list, "value": value_list, "metric": metric_list}

    LOG.info("Finished extraction for cpu utilization")
    return pd.DataFrame.from_dict(all_data)


def main():
    data_cpu_metrics = extract(query2, start, end, time_delta)
    LOG.info(data_cpu_metrics)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
