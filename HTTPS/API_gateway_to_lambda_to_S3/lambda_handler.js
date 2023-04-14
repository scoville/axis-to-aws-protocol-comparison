var AWS = require('aws-sdk');

const s3 = new AWS.S3();
const pad = (n) => {
    return (n < 10 ? '0' : '') + n;
}

const formatTime = (date) => {
    var yyyy = date.getFullYear().toString()
    var MM = pad(date.getMonth() + 1)
    var dd = pad(date.getDate())
    var hh = pad(date.getHours())
    var mm = pad(date.getMinutes())
    var ss = pad(date.getSeconds())
    var ms = pad(date.getMilliseconds())

    return yyyy + "-" + MM + "-" + dd + "_" + hh + "-" + mm + "-" + ss + "-" + ms
};
const uploadFile = async (bucketName, fileName, data, fileType) => {
    return new Promise((resolve, reject) => {
        if (!data || data == "") resolve("Data is empty");
        var putParams = {
            Body: data,
            Bucket: bucketName,
            Key: fileName,
            //ContentEncoding: 'binary',
        };
        if (fileType) {
            putParams.ContentType = fileType;
        }
        s3.upload(putParams, function (err, data) {
            if (err) {
                console.log(err, err.stack); // an error occurred
                throw new Error(err.message || 'Error in upload file function');
            }
            console.log(data); // successful response
            resolve(`Upload successful:${bucketName}/${fileName}`);
        });
    });
};
const parse = (req, fields, defaultValues = []) => {
    const header = req.headers;
    const query = {...req.queryStringParameters, ...req.query};
    const pathParams = req.pathParameters;
    const allData = {
        ...header,
        ...query,
        ...pathParams
    };
    console.log("Query params:", allData);
    let result = {};

    if (fields.length > 0) {
        fields.forEach((field, index) => {
            if (allData[field] !== undefined) {
                result[field] = allData[field];
            } else if (defaultValues.length > index) {
                result[field] = defaultValues[index];
            } else {
                result[field] = undefined;
            }
        });
    } else {
        result = allData;
    }

    return result;
};

const upload = async (event) => {

    let parsedParams = parse(event, ["subfolder"]);
    console.log("Parsed Params:", parsedParams);
    // add logging level
    console.log('Request Headers:', event.headers);
    //console.log('Request Body', event.body);
    var now = Date.now();
    let currentTime = formatTime(new Date(now));
    let fileName = `${currentTime}.mkv`;
    let subfolder = parsedParams["subfolder"] || "default_folder";
    if (event.headers["Content-Disposition"]) {
        fileName = event.headers["Content-Disposition"].replace("attachment; filename=", "").replace(/"/g, '');
    }
    console.log("Writing video:", currentTime + `${subfolder}/${fileName}`)

    let data = Buffer.from(event.body, 'base64');

    //console.log("BODY:", event.body);
    //console.log("DATA:", data);
    let contentType = 'video/x-matroska'; //event.headers["content-type"] || "video/mp4";
    let result = await uploadFile('output-bucket', `${subfolder}/${fileName}`, data, contentType);
    const response = {
        statusCode: 200,
        body: JSON.stringify(result),
    };
    return response;
};

exports.handler = async (event) => {
    console.log(event);

}
