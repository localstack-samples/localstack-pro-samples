export const lambdaHandler = async (event, context) => {
  const message = 'Hello LocalStack!';
  console.log(message);

  return {
    statusCode: 200,
    body: JSON.stringify({ message: message })
  }
}
