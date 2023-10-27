const cv = require('opencv4nodejs');

function detectObjects(imageData) {
    const mat = new cv.Mat(imageData.height, imageData.width, cv.CV_8UC4);
    mat.data.set(imageData.data);

    const net = cv.readNetFromDarknet('yolov3.cfg', 'yolov3.weights');
    const layerNames = net.getLayerNames();
    const outputLayerNames = layerNames.slice(-3).map(l => l.replace(/\d/g, ''));

    const blob = cv.blobFromImage(mat, 1/255.0, new cv.Size(416, 416), [0,0,0], true, false);
    net.setInput(blob);
    const output = net.forward(outputLayerNames);

    output.forEach(outputBlob => {
        for (let i = 0; i < outputBlob.rows; i++) {
            const confidence = outputBlob.at(i, 4);
            if (confidence > 0.5) {
                const classId = outputBlob.at(i, 5);
                const box = outputBlob.row(i).colRange(0, 4);
                const [x, y, width, height] = box.data32F;
                const topLeft = new cv.Point2(x * imageData.width, y * imageData.height);
                const bottomRight = new cv.Point2((x + width) * imageData.width, (y + height) * imageData.height);
                const color = new cv.Vec(0, 255, 0);
                const thickness = 2;
                mat.drawRectangle(topLeft, bottomRight, color, thickness);
            }
        }
    });

    cv.imshowWait('Output Image', mat);
}
