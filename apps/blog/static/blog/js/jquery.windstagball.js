/**
* JQuery.windstagball.js
* @description : 源码和创作思路来源于miaov,作者只是改良为Jquery插件，方便喜欢用jquery插件的人使用
* @author : miaov winds
* @url : http://www.miaov.com/ http://www.lijian.net/
* @qq : 342377
* @version :v1.0
* @create :2012.05.04
*/
; (function($) {
    $.fn.windstagball = function(options) {

        var defaults = {
            radius: 120,
            size: 300,
            speed: 10,
            depth: 300,
            howElliptical: 1,
            fontsize: 12
        },
        param = $.extend({}, defaults, options || {}),
        selector = $(this).selector,
        warp = $(this),
        items = $(selector + ' a'),
        dtr = Math.PI / 180,
        itemPosList = [],
        active = false,
        lasta = 1,
        lastb = 1,
        distr = true,
        mouseX = 0,
        mouseY = 0,
        sb, sa, sc, ca, cb, cc, oItem, oEvent, si;
        items.each(function() {
            oItem = {};
            oItem.width = $(this).width();
            oItem.height = $(this).height();
            itemPosList.push(oItem);
        });


        init();

        warp.mouseover(function() {
            active = true;
        });

        warp.mouseout(function() {
            active = false;
        });

        warp.mousemove(function(ev) {
            oEvent = window.event || ev;
            mouseX = oEvent.clientX - (warp.offset().left + warp.width() / 2);
            mouseY = oEvent.clientY - (warp.offset().top + warp.height() / 2);
            mouseX /= 5;
            mouseY /= 5;
        });

        setInterval(setPosition, 30);

        //初始化位置
        function init() {
            var phi = 0,
            theta = 0,
            max = itemPosList.length;
            sineCosine(0, 0, 0);
            //初始随机排序
            items.sort(function() {
                return Math.random() < 0.5 ? 1 : -1;
            });

            items.each(function(i) {
                if (distr) {
                    phi = Math.acos(-1 + (2 * i) / max);
                    theta = Math.sqrt(max * Math.PI) * phi;
                }
                else {
                    phi = Math.random() * (Math.PI);
                    theta = Math.random() * (2 * Math.PI);
                }
                itemPosList[i].cx = param.radius * Math.cos(theta) * Math.sin(phi);
                itemPosList[i].cy = param.radius * Math.sin(theta) * Math.sin(phi);
                itemPosList[i].cz = param.radius * Math.cos(phi);
                $(this).css('left', itemPosList[i].cx + warp.width() / 2 - itemPosList[i].width / 2 + 'px');
                $(this).css('top', itemPosList[i].cy + warp.height() / 2 - itemPosList[i].height / 2 + 'px');
            });
        };

        function sineCosine(a, b, c) {
            sa = Math.sin(a * dtr);
            ca = Math.cos(a * dtr);
            sb = Math.sin(b * dtr);
            cb = Math.cos(b * dtr);
            sc = Math.sin(c * dtr);
            cc = Math.cos(c * dtr);
        };

        function setPosition() {
            var a, b, c = 0, j, rx1, ry1, rz1, rx2, ry2, rz2, rx3, ry3, rz3, l = warp.width() / 2, t = warp.height() / 2;

            if (active) {
                a = (-Math.min(Math.max(-mouseY, -param.size), param.size) / param.radius) * param.speed;
                b = (Math.min(Math.max(-mouseX, -param.size), param.size) / param.radius) * param.speed;
            }
            else {
                a = lasta * 0.98;
                b = lastb * 0.98;
            }
            lasta = a;
            lastb = b;

            if (Math.abs(a) <= 0.01 && Math.abs(b) <= 0.01) {
                return;
            }
            sineCosine(a, b, c);
            for (j = 0; j < itemPosList.length; j++) {
                rx1 = itemPosList[j].cx;
                ry1 = itemPosList[j].cy * ca + itemPosList[j].cz * (-sa);
                rz1 = itemPosList[j].cy * sa + itemPosList[j].cz * ca;

                rx2 = rx1 * cb + rz1 * sb;
                ry2 = ry1;
                rz2 = rx1 * (-sb) + rz1 * cb;

                rx3 = rx2 * cc + ry2 * (-sc);
                ry3 = rx2 * sc + ry2 * cc;
                rz3 = rz2;

                itemPosList[j].cx = rx3;
                itemPosList[j].cy = ry3;
                itemPosList[j].cz = rz3;

                per = param.depth / (param.depth + rz3);

                itemPosList[j].x = (param.howElliptical * rx3 * per) - (param.howElliptical * 2);
                itemPosList[j].y = ry3 * per;
                itemPosList[j].scale = per;
                itemPosList[j].alpha = per;

                itemPosList[j].alpha = (itemPosList[j].alpha - 0.6) * (10 / 6);
            }

            items.each(function(i) {
                $(this).css('left', itemPosList[i].cx + l - itemPosList[i].width / 2 + 'px');
                $(this).css('top', itemPosList[i].cy + t - itemPosList[i].height / 2 + 'px');

                $(this).css('font-size', Math.ceil(param.fontsize * itemPosList[i].scale / 2) + 8 + 'px');

                $(this).css('filter', "alpha(opacity=" + 100 * itemPosList[i].alpha + ")");
                $(this).css('opacity', itemPosList[i].alpha);
                $(this).css("z-index", i);
            });
        }
    };
})(jQuery);

