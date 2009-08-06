//jQuery OpenID Plugin 1.1 Copyright 2009 Jarrett Vance http://jvance.com/pages/jQueryOpenIdPlugin.xhtml
$.fn.openid = function() {
  var $this = $(this);

  //name input value - needed for name based OpenID
  var $usr = $this.find('input[name=openid_username]');

  //final url input value
  var $id = $this.find('input[name=openid_url]');

  //beginning and end of name OpenID url (name being the middle)
  var $front = $this.find('p:has(input[name=openid_username])>span:eq(0)');
  var $end = $this.find('p:has(input[name=openid_username])>span:eq(1)');

  //needed for special effects only
  var $usrfs = $this.find('fieldset:has(input[name=openid_username])');
  var $idfs = $this.find('fieldset:has(input[name=openid_url])');

  var submitusr = function() {
    if ($usr.val().length < 1) {
      $usr.focus();
      return false;
    }
    $id.val($front.text() + $usr.val() + $end.text());
    return true;
  };

  var submitid = function() {
    if ($id.val().length < 1) {
      $id.focus();
      return false;
    }
    return true;

  };
  var direct = function() {
    var $li = $(this);
    $li.parent().find('li').removeClass('highlight');
    $li.addClass('highlight');
    $usrfs.fadeOut('slow');
    $idfs.fadeOut('slow');
    $id.val($this.find("li.highlight span").text());
    setTimeout(function(){$('#bsignin').click()},1000);
    return false;
  };

  var openid = function() {
    var $li = $(this);
    $li.parent().find('li').removeClass('highlight');
    $li.addClass('highlight');
    $usrfs.hide();
    $idfs.show();
    $id.focus();
    $this.unbind('submit').submit(submitid);
    return false;
  };

  var username = function() {
    var $li = $(this);
    $li.parent().find('li').removeClass('highlight');
    $li.addClass('highlight');
    $idfs.hide();
    $usrfs.show();
    $this.find('#enter_your_what').text($li.attr("title"));
    $front.text($li.find("span").text().split("username")[0]);
    $end.text("").text($li.find("span").text().split("username")[1]);
    $id.focus();
    $this.unbind('submit').submit(submitusr);
    return false;
  };

  $this.find('li.direct').click(direct);
  $this.find('li.openid').click(openid);
  $this.find('li.username').click(username);
  $id.keypress(function(e) {
    if ((e.which && e.which == 13) || (e.keyCode && e.keyCode == 13)) {
      return submitid();
    }
  });
  $usr.keypress(function(e) {
    if ((e.which && e.which == 13) || (e.keyCode && e.keyCode == 13)) {
      return submitusr();
    }
  });
  $this.find('li span').hide();
  $this.find('li').css('line-height', 0).css('cursor', 'pointer');
  $this.find('li:eq(0)').click();

  return this;
};
// submitting next=%2F&openid_username=&openid_url=http%3A%2F%2Fyahoo.com%2F
// submitting next=%2F&openid_username=&openid_url=http%3A%2F%2Fyahoo.com%2F
