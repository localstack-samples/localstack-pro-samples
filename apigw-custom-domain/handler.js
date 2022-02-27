module.exports.hello = (event, context, callback) => {
		const response = {
				"statusCode": 200,
				"headers": {},
				"body": 'hello world'
		}
		callback(null, response);
};

module.exports.goodbye = (event, context, callback) => {
		const response = {
				"statusCode": 200,
				"headers": {},
				"body": 'goodbye'
		}
		callback(null, response);
};
