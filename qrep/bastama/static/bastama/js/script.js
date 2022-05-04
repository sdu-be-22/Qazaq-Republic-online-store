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


$('.click').click(function() {
  if ($('span').hasClass("fa-star")) {
    click_like_to_product('remove', this.dataset.product)

    $('.click')
      $('.click').removeClass('active')
    setTimeout(function() {
      $('.click').removeClass('active-2')
    }, 30)
      $('.click').removeClass('active-3')
    setTimeout(function() {
      $('.click span').removeClass('fa-star')
      $('.click span').addClass('fa-star-o')
    }, 15)
  } else {
    console.log(this.dataset.product)
    click_like_to_product('add', this.dataset.product)

    $('.click').addClass('active')
    $('.click').addClass('active-2')
    setTimeout(function() {
      $('.click span').addClass('fa-star')
      $('.click span').removeClass('fa-star-o')
    }, 150)
    setTimeout(function() {
      $('.click').addClass('active-3')
    }, 150)
    $('.info').addClass('info-tog')
    setTimeout(function(){
      $('.info').removeClass('info-tog')
    },1000)
  }
})

function click_like_to_product(action, product_slug) {
  console.log(action, 'from here')
  const url = '/update_like/'
  const csrf_token = get_cookie('csrftoken')

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token,
    },
    body: JSON.stringify({'action': action, 'product_slug': product_slug})
  })
    .then(res => {
      if (res.status === 401) {
        window.location.href = '/account/login'
      }
      return res.json()
    })
    .then(data => {
      console.log(data)
    })
    .catch(err => {
      console.error(err)
    })
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


