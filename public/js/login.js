var provider = new firebase.auth.GoogleAuthProvider();
provider.addScope('https://www.googleapis.com/auth/contacts.readonly');
firebase.auth().useDeviceLanguage();

$("#signup").click(function () {
    console.log("SignUp Clicked")
	$("#first").fadeOut("fast", function () {
		$("#second").fadeIn("fast");
	});
});

$("#signin").click(function () {
	$("#second").fadeOut("fast", function () {
		$("#first").fadeIn("fast");
	});
});

$(function () {
	$("form[name='login']").validate({
		rules: {

			email: {
				required: true,
				email: true
			},
			password: {
				required: true,

			}
		},
		messages: {
			email: "이메일 형식이 맞지 않습니다!",

			password: {
				required: "비밀번호를 입력해주세요!",

			}

		},
		submitHandler: function (form) {
			form.submit();
		}
	});
});



$(function () {

	$("form[name='registration']").validate({
		rules: {
			firstname: "required",
			lastname: "required",
			email: {
				required: true,
				email: true
			},
			password: {
				required: true,
				minlength: 5
			}
		},

		messages: {
			firstname: "Please enter your firstname",
			lastname: "Please enter your lastname",
			password: {
				required: "Please provide a password",
				minlength: "Your password must be at least 5 characters long"
			},
			email: "Please enter a valid email address"
		},

		submitHandler: function (form) {
			form.submit();
		}
	});
});

//normal sigin mehtod part
function normallogin(){
	var email = $('#lemail').val()
	var password = $('#lpassword').val()

	firebase.auth().signInWithEmailAndPassword(email, password)
   .then(function(firebaseUser) {
	   // Success 
	   firebase.auth().currentUser = firebaseUser
	   location.href='/search'
   })
  .catch(function(error) {
	   // Error Handling
	   alert('로그인 실패')
  });
}

//google sigin mehtod part
function signInWithGoogle() {
    var googleAuthProvider = new firebase.auth.GoogleAuthProvider

    firebase.auth().signInWithPopup(googleAuthProvider)
        .then(function (data) {
			console.log(data)
			console.log('로그인 성공!')
            var token = data.credential.accessToken;
            // The signed-in user info.
            var user = data.user;
			firebase.auth().currentUser = data.user
			location.href = "./search";
        })
        .catch(function (error) {
            console.log(error)
        })

}

function Normalsignup() {
    firebase.auth().createUserWithEmailAndPassword($("#Register-email").val(), $("#Register-password").val())
        .catch(function (error) {
            // Handle Errors here.
            var errorCode = error.code;
            var errorMessage = error.message;
            alert(errorMessage);

            //예시
            //var obj = firebase.database().ref();
            //var myReturn = JSON.stringify(obj);
            // ...
        });
}

//use 체크
function checkIfLoggedIn() {
    //auth change되면 user pass
    firebase.auth().onAuthStateChanged(function (user) {
        if (user) {
            console.log('User signed in')
            console.log('user')
            /*
                               document.getElementById('google-signin')
                                   .setAttribute('style','display: none; visibility:hidden')
                               document.getElementById('signout')
                                   .setAttribute('style','display: none; visibility:visible')
            */

        }
        else {
            console.log("not log-in!")
        }

    })
}

window.onload = function () {
    checkIfLoggedIn()
}