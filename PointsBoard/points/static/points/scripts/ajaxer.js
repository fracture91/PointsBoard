"use strict";

/**
 * Takes a form handler, makes it all AJAXy.
 * If the handler has a onXHR* method, it will be used as the on* listener on the XHR.
 * handler.ajaxerValidate is called onSubmit if it exists. If it returns true, AJAX proceeds.
 * 
 * @param handler A form handler
 */
function Ajaxer(handler) {
	this.handler = handler;
	this.handler.form.addEventListener("submit", this.onSubmit.bind(this));
}

Ajaxer.prototype = {
	onSubmit: function(e) {
		e.preventDefault();
		
		if(typeof this.handler.ajaxerValidate == "function") {
			try {
				this.handler.ajaxerValidate();
			} catch(e) {
				this.showError(e);
				return;
			}
		}
		
		var xhr = new XMLHttpRequest();
		xhr.ajaxer = this;
		xhr.onreadystatechange = this.onReadyStateChange.bind(this, xhr);
		
		//add XHR event listeners if they exist on the handler
		for(var i in this.handler) {
			var prefix = "ajaxerXHR";
			if(i.indexOf(prefix) == 0) {
				xhr["on" + i.substring(prefix.length).toLowerCase()] = this.handler[i].bind(this.handler, xhr);
			}
		}
		
		xhr.open(this.handler.form.method, this.handler.form.getAttribute("action"), true);
		var formData = new FormData(this.handler.form);
		var submit = this.findFirstSubmitButton(this.handler.form);
		if(submit) {
			formData.append(submit.name, submit.value);
		}
		xhr.send(formData);
		
		if(typeof this.handler.ajaxerAfterSend == "function") {
			this.handler.ajaxerAfterSend(e, xhr);
		}
	},
	
	findFirstSubmitButton: function(form) {
		var inputs = form.getElementsByTagName("input");
		var submits = Array.prototype.filter.call(inputs, function(el) {
			return el.type == "submit";
		});
		return submits[0];
	},
	
	onReadyStateChange: function(xhr) {
		if(xhr.readyState == 4) {
			if(xhr.status >= 200 && xhr.status < 300 || xhr.status === 304) {
				this.handler.ajaxerOnSuccess(xhr);
			}
			else {
				if(typeof this.handler.ajaxerOnFailure == "function") {
					this.handler.ajaxerOnFailure(xhr);
				}
				else {
					this.showError("Error: " + xhr.status);
				}
			}
		}
	},
	
	/**
	 * Show the given errStr with the handler's ajaxerShowError method if it exists.
	 */
	showError: function(errStr) {
		if(typeof this.handler.ajaxerShowError == "function") {
			this.handler.ajaxerShowError(errStr);
		}
	},
	
	/**
	 * Return the body DOM element with contents described by the given HTML.
	 */
	parseBody: function(html) {
		//this is disgusting and insecure, but works
		var regex = /<body>([\s\S]*)<\/body>/;
		var match = html.match(regex);
		var bodyHTML = html
		if(match) {
			bodyHTML = match[1];
		}
		var body = document.createElement("body");
		body.innerHTML = bodyHTML;
		return body;
	}
}
