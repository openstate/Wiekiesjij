function autocomplete(inpt, data, result_win, limit, limit_url) {
    var me = jQuery(inpt);
    var source = data.split(", ");

    //init result window
    result_win = jQuery(result_win);
    jQuery(document.body).append(result_win);
    var pos = me.offset();
    result_win.css({
        left: (pos.left + 1) +"px",
        top: (pos.top + me.height() + 20) + "px",
        width: me.width() + 13 + "px",
        display: "none"
    });

    //bind search
    me.keyup(function() {
        var term = me.val().toString().toLowerCase().trim();
        alert(term);
        var ls = jQuery(".results_ul", result_win);
        var more = jQuery('.more_results a', result_win);
        var i = 0;

        ls.empty();
        more.parent().hide();
        jQuery.each(source, function(key) {
            if(this['name'].toLowerCase().substr(0, term.length) == term) {
                var lnk = jQuery('<a href="#"></a>');
                lnk.attr('href', this['url']);
                lnk.text(this['name']);

                var li = jQuery('<li></li>');
                li.append(lnk).appendTo(ls);
                i++;
            }

            if(i == limit && limit_url) { //show limit url
                more.attr('href', limit_url.replace('@@', encodeURIComponent(term)));
                more.parent().show();
            }

            return i < limit;
        });

        if(i > 0) result_win.show();
        else result_win.hide();
    });

    //hide list
    jQuery(document.body).click(function() {
    	result_win.hide();
    });
}