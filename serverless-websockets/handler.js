module.exports.handler = function(event, context, callback) {
  console.log('lambda event:', event);
  // WebSocket proxy integrations must return a status code. On routes with a route
  // response, API Gateway sends the body back to the client, so echo the message.
  const response = { statusCode: 200, body: event.body || '' };
  if (callback) {
    callback(null, response);
  } else {
    context.succeed(response);
  }
};
