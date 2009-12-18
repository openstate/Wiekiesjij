/**
 * Fixes IE6 button problems.
 *
 * IE6 has two problems with form buttons:
 *   - all buttons are sent, not only the one that was clicked
 *   - value attribute is ignored, the button labels are sent (<button> tag)
 *
 * This script creates a hidden field for each submit button in disabled state
 * and clears the names of the buttons. When button is pressed, the corresponding
 * hidden field will be enabled.
 *
 * @depend jQuery
 * @author Sardar Yumatov (ja.doma@gmail.com)
 */

jQuery(document).ready(function() {
    if(jQuery.browser.msie && parseFloat(jQuery.browser.version.substr(0, 3)) < 7) {
        jQuery('form *:submit').each(function() {
            //this method is better than setting all the buttons to disabled state
            //we don't know if there is a logic in the form, that may set some
            //buttons normally in disabled state
            var but = jQuery(this);
            var hid = jQuery("<input type='hidden' name='" + but.attr('name') + "' value='" + but.val() + "' disabled='disabled'>");
            but.removeAttr('name');
            jQuery(this.form).append(hid);
            jQuery(this).click(function() {
                hid.removeAttr('disabled');
                but.attr('disabled', 'disabled');
                setTimeout(function() { //if something is failed, reset input field
                    hid.attr('disabled', 'disabled');
                    but.removeAttr('disabled');
                }, 3000);

                this.form.submit();
            });
        });
    }
});



