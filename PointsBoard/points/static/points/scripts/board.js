var ELEMENT_NODE = 1;
var TEXT_NODE = 3;

var tableElem;
var actionElem;
var catElem;
var rcvUserElem;

function setCategoryTo(catName) {
	catElem.value = catName;
}

function setRcvUserTo(username) {
	rcvUserElem.value = username;
}

function getColumnOfCell(cell) {
	//get string containing the category name
	//given the HTMLElement object representing the cell the user clicked on
}

function getUserNameOfCell(cell) {
	//get the username (as a string) associated with the cell's row
	//given the HTMLElement object representing the cell the user clicked on
	
}

function boardClickHandler(e) {
	var clickTarget;
	if(!e) {
		alert("!e")
		return;
	}
	//left mouse button
	if(e.button == 0) {
		clickTarget = e.target;
		var rcvUserName = getUserNameOfCell(clickTarget)
		if(rcvUserName) {
			setRcvUserTo(rcvUserName);
		}
		var categoryName = getColumnOfCell(clickTarget);
		if(categoryName) {
			setCategoryTo(categoryName);
		}
	}
}

window.onload = function () {
	tableElem = document.getElementById("board");
	tableElem.addEventListener("click", boardClickHandler, true);
	actionElem = document.getElementById("trans_action");
	catElem = document.getElementById("trans_category");
	rcvUserElem = document.getElementById("trans_rcvUser");
}
