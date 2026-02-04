function readDataFile(fileName) {
    var scriptFile = new File($.fileName);
    var scriptFolder = scriptFile.parent;

    var dataFile = new File(scriptFolder + "/" + fileName);

    if (!dataFile.exists) {
        throw new Error("Arquivo " + fileName + " não encontrado.");
    }

    dataFile.open("r");
    var content = dataFile.read();
    dataFile.close();

    var blocks = content.split("-------------");
    var dataArray = [];

    for (var i = 0; i < blocks.length; i++) {
        var block = blocks[i].trim();
        if (!block) continue;

        var lines = block.split(/\r?\n/);
        var obj = {};

        for (var j = 0; j < lines.length; j++) {
            var line = lines[j].trim();
            if (!line) continue;

            var parts = line.split(":");
            if (parts.length < 2) continue;

            var key = parts[0].trim();
            var value = parts.slice(1).join(":").trim();

            if (key === "betAmount" || key === "profit") {
                value = parseFloat(value);
            }

            obj[key] = value;
        }

        dataArray.push(obj);
    }

    return dataArray;
}
