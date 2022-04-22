function big(element){
    element.style.fontSize = "50px";
}

function small(element){
    element.style.fontSize="45px";
}
function change(element){
    var a = element.innerHTML;
    switch(a){
        case "-Almaty-":
            document.getElementById("map").src="static/bastama/images/home/almaty.png";
            document.getElementById("h").innerHTML="meken-jai: Almaty, Mametova 47 & Rozybakieva 247a";
            document.getElementById("t").innerHTML="+7‒708‒688‒61‒18 || +7‒778‒948‒98‒00";
            break;
        case "-Nur-Sultan-":
            document.getElementById("map").src="static/bastama/images/home/astana.png";
            document.getElementById("qala").href="whatsapp://send?phone=77081223910&text=";
            document.getElementById("h").innerHTML="meken-jai: Nur-Sultan, Uly Dala 7/7 & Qabanbai Batyr 62";
            document.getElementById("t").innerHTML="+7‒777‒062‒13‒09";
            break;
        case "-Shymkent-":
            document.getElementById("map").src="static/bastama/images/home/shym.png";
            document.getElementById("qala").href="whatsapp://send?phone=77088001465&text=";
            document.getElementById("h").innerHTML="meken-jai: Shymkent, Tauke khan 43a";
            document.getElementById("t").innerHTML=" ";
           break;
        case "-Aqtobe-":
            document.getElementById("map").src="static/bastama/images/home/aqtobe.png";
            document.getElementById("qala").href="whatsapp://send?phone=77088001465&text=";
            document.getElementById("h").innerHTML="meken-jai: Aqtobe, Mametova 4";
            document.getElementById("t").innerHTML="+7‒7132-77-70-78";
           break;
        case "-Aqtau-":
            document.getElementById("map").src="static/bastama/images/home/aqtau.png";
            document.getElementById("qala").href="whatsapp://send?phone=77088001465&text=";
            document.getElementById("h").innerHTML="meken-jai: Aqtau, 17 mkr. 95";
            document.getElementById("t").innerHTML="+7‒778‒546‒07‒83";
            break;
    }

}
function ch(element){
    var b=element.innerHTML;
    switch(b){
        case "Go":
            document.getElementById("h1").innerHTML="No such result found";
            break;
    }
}

let sidebar = document.querySelector('#sidebar');
let hamburger = document.querySelector('.hamburger')

function openSide () {
    if (sidebar.classList.contains('active')) {
        sidebar.classList.remove('active')
        hamburger.classList.remove('open')
    } else {
        sidebar.classList.add('active')
        hamburger.classList.add('open')
    }
}

Vue.use(VueMaterial.default)

        var example = {
            methods:{
                download: function(){
                    let email = document.getElementById("emailAddress");
                    let fullname = document.getElementById("messagee");
                    let mes = document.getElementById("message");

                    let data = "Question from user " + "\n" +
                    "\nEmail: " + email.value + "\n " +
                    "\nFullname: " + fullname.value + "\n" +
                    "\nMessage: " + mes.value + "\n " ;


                    var blob = new Blob([ data ], { "type" : "text/plain" });
                    let link = document.createElement('a')
                    link.href = window.URL.createObjectURL(blob)
                    link.download = 'information.txt'
                    link.click()
                }
            }
        }

        var app = new Vue(example)

        app.$mount("#app");


