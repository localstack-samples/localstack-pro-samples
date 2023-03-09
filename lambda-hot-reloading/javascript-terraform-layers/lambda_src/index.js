const testDep = require('test-dep')

exports.handler = async function (event, context) {
    var number1 = testDep();
    var number2 = 31;
    var sum = number1 + number2;
    var product = number1 * number2;
    var difference = Math.abs(number1 - number2);
    var quotient = number1 / number2;
    return {
        "Number1": number1,
        "Number2": number2,
        "Sum": sum,
        "Product": product,
        "Difference": difference,
        "Quotient": quotient
    };
 };
