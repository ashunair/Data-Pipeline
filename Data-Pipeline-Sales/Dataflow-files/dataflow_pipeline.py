import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from apache_beam.io.gcp.bigquery import WriteToBigQuery
import json
import logging


class ParseEvent(beam.DoFn):
    def process(self, element):
        try:
            # Decode and parse the JSON message
            data = json.loads(element.decode("utf-8"))
            # Validate required fields
            if all(key in data for key in ["event_id", "user_id", "item_id", "event_type", "timestamp"]):
                yield data
            else:
                logging.warning(f"Invalid message: {data}")
        except json.JSONDecodeError:
            logging.error(f"Failed to decode message: {element}")


def run():
    PROJECT_ID = "nth-suprstate-438619-c9"
    BUCKET_NAME = "dataflow-bucket-ashu"
    REGION = "us-central1"
    PUBSUB_TOPIC = f"projects/{PROJECT_ID}/topics/sales-events-topic"
    BIGQUERY_TABLE = f"{PROJECT_ID}:sales_data.sales_events"

    # Define the pipeline options
    options = PipelineOptions(
        project=PROJECT_ID,
        region=REGION,
        temp_location=f"gs://{BUCKET_NAME}/temp",
        staging_location=f"gs://{BUCKET_NAME}/staging",
        runner="DataflowRunner",
        streaming=True,
    )
    options.view_as(StandardOptions).streaming = True

    # Define the Apache Beam pipeline
    with beam.Pipeline(options=options) as pipeline:
        (
            pipeline
            | "Read from Pub/Sub" >> beam.io.ReadFromPubSub(topic=PUBSUB_TOPIC)
            | "Parse JSON Messages" >> beam.ParDo(ParseEvent())
            | "Write to BigQuery" >> WriteToBigQuery(
                table=BIGQUERY_TABLE,
                schema="event_id:STRING, user_id:STRING, item_id:STRING, event_type:STRING, timestamp:TIMESTAMP",
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
            )
        )


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run()
