"use strict";

/**
 * Holds information about a cell in a Board.
 * 
 * @param el The TD element
 * @param category The category of points this Cell is in
 * @param username The username this Cell holds points for
 */
function Cell(el, category, username) {
	this.el = el;
	this.category = category;
	this.username = username;
}

/**
 * Easy interface for getting information about a board.
 * 
 * @param table The table element for a board
 */
function Board(table) {
	this.table = table;
}

Board.prototype = {
	/**
	 * Given an element, return a Cell for it, or null if not a cell.
	 */
	getCell: function(el) {
		if(this.table.contains(el) && el.tagName == "TD" && el.classList.contains("points")) {
			var username = this.trim(el.parentNode.firstElementChild.textContent);
			var category = this.getCategory(this.findChildIndex(el));
			return new Cell(el, category, username);
		}
	},
	trim: function(str) {
		return str.replace(/^\s+|\s+$/g, "");
	},
	findChildIndex: function(el) {
		var children = el.parentNode.children;
		for(var i = 0; i < children.length; i++) {
			if(children[i] == el) {
				return i;
			}
		}
		return null;
	},
	getCategory: function(index) {
		return this.trim(this.getHead().getElementsByTagName("th")[index].textContent);
	},
	getHead: function() {
		return this.table.getElementsByTagName("thead")[0];
	},
	
	/**
	 * Replace the contents of this table with the contents of newTable.
	 */
	replaceWith: function(newTable) {
		this.table.innerHTML = "";
		while(newTable.children.length > 0) {
			this.table.appendChild(newTable.firstElementChild);
		}
	}
}

/**
 * Easy interface for changing the transaction form.
 * 
 * @param form The form element for the transaction form
 */
function TransactionForm(form) {
	this.form = form;
	this.pointsInput = this.form["numPts"];
	this.categoryInput = this.form["category"];
	this.usernameInput = this.form["rcvUser"];
	this.reasonInput = this.form["reason"];
}

TransactionForm.prototype = {
	setCategory: function(category) {
		this.categoryInput.value = category;
	},
	setUsername: function(username) {
		this.usernameInput.value = username;
	}
}

/**
 * Listens for clicks in the cells of the given Board,
 * fills in the given TransactionForm with appropriate info for that clicked cell.
 */
function Filler(board, form) {
	this.board = board;
	this.form = form;
	this.board.table.addEventListener("click", this.onBoardClick.bind(this));
}

Filler.prototype = {
	onBoardClick: function(e) {
		var cell = this.board.getCell(e.target);
		if(cell) {
			e.preventDefault();
			this.onCellClick(cell);
		}
	},
	onCellClick: function(cell) {
		this.form.setCategory(cell.category);
		this.form.setUsername(cell.username);
		this.form.pointsInput.focus();
	}
}


/**
 * Handles XHRs for an Ajaxer on the transaction form.
 * Adds new transactions and updates the board.
 * 
 * @param board A Board instance to update
 * @param transForm A TransactionForm instance
 */
function TransactionHandler(board, transForm) {
	this.board = board;
	this.transForm = transForm;
	this.container = this.transForm.form.parentNode;
	this.form = this.transForm.form;
}

TransactionHandler.prototype = {
	ajaxerAfterSend: function(e, xhr) {
		var p = document.createElement("p");
		p.className = "feedback";
		p.textContent = "Submitting...";
		this.form.appendChild(p);
	},
	ajaxerValidate: function(e) {
		if(this.transForm.reasonInput.value == "") {
			throw "You must input a reason for the transaction.";
		}
		if(this.transForm.categoryInput.value == "") {
			throw "You must choose a category.";
		}
		if(this.transForm.usernameInput.value == "") {
			throw "You must choose a username."
		}
	},
	ajaxerShowError: function(errStr) {
		alert(errStr);
	},
	ajaxerOnSuccess: function(xhr) {
		var newBody = xhr.ajaxer.parseBody(xhr.responseText);
		var transactions = newBody.getElementsByClassName("transaction");
		var numToAdd = transactions.length - document.getElementsByClassName("transaction").length;
		transactions = Array.prototype.slice.call(transactions, 0, numToAdd);
		var insertAfterMe = this.container;
		transactions.forEach(function(trans) {
			insertAfterMe.parentNode.insertBefore(trans, insertAfterMe.nextSibling);
			insertAfterMe = trans;
		});
		this.board.replaceWith(newBody.getElementsByTagName("table")[0]);
	},
	ajaxerXHRLoadEnd: function(xhr) {
		var p = this.container.getElementsByClassName("feedback")[0];
		p.parentNode.removeChild(p);
	}
}


/**
 * Handles XHRs for an Ajaxer on the Owner Controls forms.
 * 
 * @param board A Board instance to update
 * @param form The form element to get input from
 */
function ControlsHandler(board, form) {
	this.board = board;
	this.form = form;
}

ControlsHandler.prototype = {
	ajaxerAfterSend: function(e, xhr) {
		var p = document.createElement("p");
		p.className = "feedback";
		p.textContent = "Submitting...";
		this.form.parentNode.insertBefore(p, this.form.nextSibling);
	},
	ajaxerValidate: function(e) {
		if(this.form.getElementsByTagName("input")[1].value == "") {
			throw "You cannot leave the field blank.";
		}
	},
	ajaxerShowError: function(errStr) {
		alert(errStr);
	},
	ajaxerOnSuccess: function(xhr) {
		var newBody = xhr.ajaxer.parseBody(xhr.responseText);
		var table = newBody.getElementsByTagName("table")[0];
		if(table) {
			this.board.replaceWith(table);
		}
	},
	ajaxerXHRLoadEnd: function(xhr) {
		var p = this.form.nextSibling;
		if(p.classList.contains("feedback")) {
			p.parentNode.removeChild(p);
		}
	}
}

window.addEventListener("load", function(e) {
	window.board = new Board(document.getElementById("board"));
	window.transForm = new TransactionForm(document.getElementById("newtransaction")
			.getElementsByTagName("form")[0]);
	window.filler = new Filler(board, transForm);
	
	window.transactionAjax = new Ajaxer(new TransactionHandler(board, transForm));
	
	var forms = document.getElementById("owner_controls").getElementsByTagName("form");
	window.ownerControlsAjax = [];
	//skip first form
	for(var i = 1; i < forms.length; i++) {
		ownerControlsAjax.push(new Ajaxer(new ControlsHandler(board, forms[i])));
	}
})
