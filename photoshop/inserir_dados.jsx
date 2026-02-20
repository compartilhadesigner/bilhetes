#target photoshop
#include "reader.jsx"
#include "utils.jsx"
#include "prototypes.jsx"
#include "salvar.jsx"

if (!app.documents.length) {
    alert("Abra o PSD antes de rodar o script.");
    throw new Error("Nenhum documento aberto");
}

var doc = app.activeDocument;

var scriptFolder = new File($.fileName).parent;
var screenshotsFolder = new Folder(scriptFolder.parent + "/screenshots");

if (!screenshotsFolder.exists) {
    alert("Pasta screenshots não encontrada.");
    throw new Error("screenshots ausente");
}

var data = readDataFile("dados.json");

for (var customer in data) {

    var tickets = data[customer];

    for (var i = 0; i < tickets.length; i++) {

        var item = tickets[i];

        // gera nome automaticamente
        item.print = customer + (i + 1) + ".png";

        // 1. pasta do customer
        var customerGroup = findLayerSet(doc, customer);
        if (!customerGroup) continue;

        // 2. TEXTO
        var textoGroup = findLayerSet(customerGroup, "TEXTO");

        if (customer === "CENTRAL BET") {

            var fator = toFloat(item.profit) / toFloat(item.betAmount);

            if (textoGroup) {

                var retorno10 = findTextLayer(textoGroup, "RETORNO 10");
                if (retorno10) retorno10.textItem.contents = String(fator * 10);

                var retorno20 = findTextLayer(textoGroup, "RETORNO 20");
                if (retorno20) retorno20.textItem.contents = String(fator * 20);

                var retorno50 = findTextLayer(textoGroup, "RETORNO 50");
                if (retorno50) retorno50.textItem.contents = String(fator * 50);

                var retorno100 = findTextLayer(textoGroup, "RETORNO 100");
                if (retorno100) retorno100.textItem.contents = String(fator * 100);

                var pin = findTextLayer(textoGroup, "PIN");
                if (pin) pin.textItem.contents = String(item.code);
            }

        } else {

            if (textoGroup) {

                var retorno = findTextLayer(textoGroup, "RETORNO");
                if (retorno) retorno.textItem.contents = String(item.profit);

                var valor = findTextLayer(textoGroup, "VALOR");
                if (valor) valor.textItem.contents = String(item.betAmount);

                var pin = findTextLayer(textoGroup, "PIN");
                if (pin) pin.textItem.contents = String(item.code);
            }
        }

        // 3. BILHETE
        var bilheteGroup = findLayerSet(customerGroup, "BILHETE");
        if (bilheteGroup) {
            var imgFile = new File(screenshotsFolder + "/" + item.print);
            replaceImageInGroup(bilheteGroup, imgFile);
        }

        save_image(customer, i)
    }
}

alert("Processo finalizado com sucesso!");
