/*
    Makes fieldsets with a collapse class collapsable
*/
jQuery.event.special.toggleCollapse = {
	setup: function(data, namespaces) {
		for(var i in namespaces)
		{
			if(namespaces[i] == "FieldsetEvent")
			{   
			    jQuery(this).children('*:first').bind('click', jQuery.event.special.toggleCollapse.FieldsetEvent.handler);
			    jQuery(this).children('*:first').click();
			}
		}						
	},
	
	teardown: function(namespaces) {
		for(var i in namespaces)
		{
			if(namespaces[i] == "FieldsetEvent")
			{
				jQuery(this).children('*:first').unbind('click', jQuery.event.special.toggleCollapse.FieldsetEvent.handler);
			}
		}
	},
		
	FieldsetEvent: {
		handler: function(event) {
			if(event.target == event.currentTarget)
			{
				var elt = jQuery(this);						
				var cssClass = "collapsed";
				if(elt.parent('fieldset').hasClass(cssClass))
				{
					elt.nextAll().slideDown().end().parent('fieldset').removeClass(cssClass);
				}
				else
				{
					elt.nextAll().slideUp().end().parent('fieldset').addClass(cssClass);
				}
				
				event.type = "toggleCollapse";
				jQuery.event.handle.apply(this, arguments);
			}
		}
	}
};

jQuery(document).ready(function() {
   jQuery('fieldset.collapse').bind("toggleCollapse.FieldsetEvent", function(evt) {});  
});
