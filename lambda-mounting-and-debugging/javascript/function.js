exports.handler = async (event) => {
    console.log(event);
    const response = {
        statusCode: 200,
        body: "ok",
    };
    return response;
};
