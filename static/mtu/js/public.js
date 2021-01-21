$(document).ready(function () {
    // $(".search-show").hover(function () {
    //     $(".search-box").fadeIn(300);
    // }, function () {
    //     $(".search-box").stop(true, true).fadeOut(300);
    // });
    var random_bg = Math.floor(Math.random() * 3 + 1);
    var bg = 'url(images/banner-' + random_bg + '.jpg)';
    $(".banner").css("background-image", bg);
    $(".last-slide").hover(function () {
        $(".last-nav-down").slideDown(200);
    }, function () {
        $(".last-nav-down").stop(true, true).slideUp(200);
    });
    $(".list-slide").hover(function () {
        $(".list-slide-down").slideDown(200);
    }, function () {
        $(".list-slide-down").stop(true, true).slideUp(200);
    });
    $(".last-nav-down a:odd,.list-slide-down a:odd").css("background-color", "#f7f7f7");
});

var CookieHelper = {
    set: function (key, val, time) {
        if (time == 0) {
            document.cookie = key + "=" + val;
            return;
        }
        var date = new Date();
        var expiresDays = time;
        date.setTime(date.getTime() + expiresDays * 24 * 3600 * 1000);
        document.cookie = key + "=" + val + ";expires=" + date.toGMTString();
    },
    get: function (key) {
        var getCookie = document.cookie.replace(/[ ]/g, "");
        var arrCookie = getCookie.split(";")
        var tips;
        for (var i = 0; i < arrCookie.length; i++) {
            var arr = arrCookie[i].split("=");
            if (key == arr[0]) {
                tips = arr[1];
                break;
            }
        }
        return tips;
    },
    delete: function (key) {
        var date = new Date();
        date.setTime(date.getTime() - 10000);
        document.cookie = key + "=v; expires =" + date.toGMTString();
    }
}

function incPV() {
    num = parseFloat(CookieHelper.get("_uupv"));
    if (isNaN(num)) {
        CookieHelper.set("_uupv", 1, 0);
    } else {
        if (num >= 40) {
            CookieHelper.set("_uupv", 1, 0);
        } else {
            CookieHelper.set("_uupv", num + 1, 0);
        }
    }
}

incPV();

function checkPV(t) {
    num = parseFloat(CookieHelper.get("_uupv"));
    if (isNaN(num)) {
        return false;
    }
    return num >= t ? true : false;
}

function getPV() {
    num = parseFloat(CookieHelper.get("_uupv"));
    if (isNaN(num)) {
        return 0;
    }
    return num;
}

/* 美女上下篇下方，960px */
/*function mnPage2() {
    var pathname = document.location.pathname;
    if (pathname.indexOf('.html') != -1) {
        var _pv = getPV();
        var _mod = _pv % 2;

        if (_mod == 0) {
            document.writeln('<a href="" target="_blank" title="数码"><img src="https://newimg.uumtu.com/Thumb/tb_dg1.jpg" alt="数码"></a>');
        } else {
            document.writeln('<a href="" target="_blank" title="数码"><img src="https://newimg.uumtu.com/Thumb/tb_dg1.jpg" alt="数码"></a>');
        }
    }
}*/