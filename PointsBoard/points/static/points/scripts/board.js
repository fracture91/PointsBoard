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
	this.head = this.table.getElementsByTagName("thead")[0];
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
		return this.trim(this.head.getElementsByTagName("th")[index].textContent);
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

window.addEventListener("load", function(e) {
	window.board = new Board(document.getElementById("board"));
	window.transForm = new TransactionForm(document.getElementById("newtransaction")
			.getElementsByTagName("form")[0]);
	window.filler = new Filler(board, transForm); 
})
