resource "aws_dynamodb_table" "demo_table" {
  name           = "MusicTable"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "Artist"
  range_key      = "Song"

  attribute {
    name = "Artist"
    type = "S"
  }

  attribute {
    name = "Song"
    type = "S"
  }

  stream_enabled = true
  stream_view_type = "NEW_AND_OLD_IMAGES"
}

resource "aws_kinesis_stream" "demo_stream" {
  name             = "demo_stream"
  shard_count      = 1

  retention_period = 24

  shard_level_metrics = ["IncomingBytes", "OutgoingBytes"]
}

resource "aws_dynamodb_kinesis_streaming_destination" "streaming_destination" {
    stream_arn = aws_kinesis_stream.demo_stream.arn
    table_name = aws_dynamodb_table.demo_table.name   
}
