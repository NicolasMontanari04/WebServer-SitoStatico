window.onload = function (){ //viene eseguito quando la pagina si carica
    const tag = document.querySelectorAll('.card'); //prendo l'array di card
    const regs = document.querySelectorAll('.reg'); //prendo l'array di regione

    const move = (e, i) =>{ //funzione move -> cambia le coordinate della card in base a quelle del mouse
        tag[i].style.left = e.pageX + 10 + 'px';
        tag[i].style.top = e.pageY + 10 + 'px';
        tag[i].style.display = 'block'; //fa visualizzare la card, prima nascosta
    }

    regs.forEach((reg, i) => { //per ogni regione
        reg.addEventListener("mousemove", (e) => move(e, i)); //controlla se su una data regione vi è il mouse sopra, se si esegui move
        reg.addEventListener("mouseleave", (e) => { //quando il mouse va via da una regione rinascondi tutte le card
            tag.forEach(el => {
                el.style.display = 'none';
            });
        });
    });
}

function check(){
    trueAnswers = document.getElementsByClassName("true"); //risposte vere
    falseAnswers = document.getElementsByClassName("false"); //risposte false
    var point=0; //contatore punti
    for (const child of trueAnswers) { //coloro le risposte giuste di verde
        child.style.color = "#40ce23"
    }
    for (const child of falseAnswers) { //coloro le risposte sbagliate di rosso
        child.style.color = "#ce2323"
    }

    trueRadio = document.getElementsByClassName("rtrue"); //radio button giusti
    for (const child of trueRadio) { //quelli checkati giusti li conto nel punteggio
        if(child.checked){
            point++;
        }
    }
    document.getElementById("res").innerHTML=`Punteggio: ${point}` //stampo il punteggio
}
