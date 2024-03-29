var browseridArguments = {
  // display our tos and privacy policy in the browserid dialog
  privacyURL: 'https://browserid.org/privacy.html',
  tosURL: 'https://browserid.org/tos.html',
};

function setSessions(val) {
  if (navigator.id) {
    navigator.id.sessions = val ? val : [ ];
  }
}

// when the user is found to be logged in we'll update the UI, fetch and
// display the user's favorite beer from the server, and set up handlers to
// wait for user input (specifying their favorite beer).
function loggedIn(email, immediate) {
  setSessions([ { email: email } ]);

  // set the user visible display
  var l = $(".login").removeClass('clickable');;
  l.empty();
  l.css('opacity', '1');
  l.append($("<span>").text("Yo, "))
    .append($("<span>").text(email).addClass("username"))
    .append($("<span>!</span>"));
  l.append($('<div><a id="logout" href="#" >(logout)</a></div>'));
  l.unbind('click');

  $("#logout").bind('click', logout);
  $.ajax({
    type: 'GET',
    url: 'https://browserid.org/api/get',
    success: function(res, status, xhr) {
      $("input").val(res);
    }
  });

  // get a gravatar cause it's pretty
  var iurl = 'http://www.gravatar.com/avatar/' +
    Crypto.MD5($.trim(email).toLowerCase()) +
    "?s=32";
  $("<img>").attr('src', iurl).appendTo($(".picture"));
}

function save(event) {
  event.preventDefault();
  $.ajax({
    type: 'POST',
    url: 'https://browserid.org/api/set',
    data: { beer: $("input").val() },
    success: function(res, status, xhr) {
      // noop
    }
  });
}

// when the user clicks logout, we'll make a call to the server to clear
// our current session.
function logout(event) {
  event.preventDefault();
  $.ajax({
    type: 'POST',
    url: 'https://browserid.org/api/logout',
    success: function() {
      // and then redraw the UI.
      loggedOut();
    }
  });
}

// when no user is logged in, we'll display a "sign-in" button
// which will call into browserid when clicked.
function loggedOut() {
  setSessions();
  $("input").val("");
  $('.intro').fadeIn(300);
  $(".picture").empty();
  var l = $(".login").removeClass('clickable');
  l.html('<img src="http://myfavoritebeer.org/i/sign_in_blue.png" alt="Sign in">')
    .show().one('click', function() {
      $(" .login").css('opacity', '0.5');
      navigator.id.get(gotVerifiedEmail, browseridArguments);
    }).addClass("clickable").css('opacity','1.0');
}

// a handler that is passed an assertion after the user logs in via the
// browserid dialog
function gotVerifiedEmail(assertion) {
  // got an assertion, now send it up to the server for verification
  if (assertion !== null) {
    $.ajax({
      type: 'POST',
      url: 'https://browserid.org/i/api/login',
      data: { assertion: assertion },
      success: function(res, status, xhr) {
        if (res === null) loggedOut();
        else loggedIn(res);
      },
      error: function(xhr, status, error) {
        alert("login failure " + error);
      }
    });
  }
  else {
    loggedOut();
  }
}

// For some reason, login/logout do not respond when bound using jQuery
if (document.addEventListener) {
  document.addEventListener("login", function(event) {
    $(".login").css('opacity', '0.5');
    navigator.id.get(gotVerifiedEmail, browseridArguments);
  }, false);

  document.addEventListener("logout", logout, false);
}

// at startup let's check to see whether we're authenticated to
// myfavoritebeer (have existing cookie), and update the UI accordingly
$(function() {
  $.get('https://browserid.org/verify', function (res) {
    if (res === null) loggedOut();
    else loggedIn(res, true);
  }, 'json');
});
