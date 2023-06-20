def lambda_handler(event, context):
    print(event)
    return "Together Adam and Cole say '{}'!!".format(' '.join(event["input"]))
