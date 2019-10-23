const { echo } = require('./lib');

module.exports.hello = async function(event, context) {
  echo('This text should be printed in the Lambda');
}
