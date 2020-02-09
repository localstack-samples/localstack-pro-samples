module.exports.handler = function(event, context, callback) {
  console.log('lambda event:', event, callback, context);
  if(callback) {
		callback(null, event);
	} else {
		context.succeed(event);
	}
};
