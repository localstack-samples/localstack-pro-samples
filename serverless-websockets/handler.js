module.exports.handler = function(event, context, callback) {
  console.log('lambda event:', event);
  if(callback) {
		callback(null, event);
	} else {
		context.succeed(event);
	}
};
