function listDetails() {
document.forms[0].target="main";
document.forms[0].mode.value="R";
document.forms[0].tan.value="Apply";
document.forms[0].start.value=0;
document.forms[0].submit();
}
var createwin;
function create(action,w,h,scroll) {
if(parent.frames[0] && parent.frames[1].document.forms[0]) {
if(document.forms[0].start && parent.frames[1].document.forms[0].start) {
    document.forms[0].start.value=parent.frames[1].document.forms[0].start.value;
}
if(document.forms[0].total && parent.frames[1].document.forms[0].total) {
    document.forms[0].total.value=parent.frames[1].document.forms[0].total.value;
}
}
createwin = window.open(action,
                "win",
                "menubar=no,status=no,toolbar=no,titlebar=no,location=no,scrollbars="+scroll+",resizable=yes,left="+screen.width/4+",top="+screen.height/4+",width="+w+",height="+h);
}
function saveDetails() {
if(document.forms[0].mode.value=="Edit") {
var form = document.forms[0];
form.result.value="";
form.mode.value="Edit";
form.tan.value="Apply";
form.submit();
} else {
var form = document.forms[0];
form.result.value="";
form.mode.value="I";
form.tan.value="Apply";
form.submit();
}
}
function refreshParent() {
	try {
if(opener.parent.frames[0]) {

opener.parent.frames[0].document.forms[0].target="main";
opener.parent.frames[0].document.forms[0].mode.value="R";
opener.parent.frames[0].document.forms[0].tan.value="Apply";
opener.parent.frames[0].document.forms[0].submit();
} else {
opener.document.forms[0].mode.value="Select";
if(opener.document.forms[0].tan) {
opener.document.forms[0].tan.value="";
}
opener.document.forms[0].submit();
}
	} catch (error) {
		// Do nothing for Permission denied exception
		if (!error.message == "Permission denied") {
            throw error;
        }  
	}
}

function isChanged() {
var rtnVal = false;
var frm = document.forms[0];
var ele = frm.elements;
for (i=0; i<ele.length;i++ ) {
if (ele[i].type.length >0) {
if (isElementChanged(ele, i)) {
rtnVal = true;
break;
}
}
}
return rtnVal;
}
function isElementChanged(ele, i) {
var isEleChanged = false;
switch (ele[i].type) {
case "text" :
if (ele[i].value != ele[i].defaultValue) return true;
break;
case "textarea" :
if (ele[i].value != ele[i].defaultValue) return true;
break;
case "radio" :
val = "";
if (ele[i].checked != ele[i].defaultChecked) return true;
break;
case "select-one" :
var selIndex=0;
for(j=0;j<document.forms[0].elements[i].options.length;j++) {
if(document.forms[0].elements[i].options[j].defaultSelected){selIndex=j;}
}
if(document.forms[0].elements[i].options.selectedIndex!=selIndex){return true;}
break;
case "select-multiple" :
for (var x =0 ; x <ele[i].length; x++) {
if (ele[i].options[x].selected != ele[i].options[x].defaultSelected)
    return true;
}

break;
case "hidden":
if (ele[i].value != ele[i].defaultValue) return true;
break;
case "password":
if (ele[i].value != ele[i].defaultValue) return true;
break;
case "checkbox" :
if (ele[i].checked != ele[i].defaultChecked) return true;
default:
return false;
break;
}
}
function closeWindow(screen) {
if(isChanged()|| (document.forms[0].result.value && document.forms[0].result.value=="N")) {
if(confirm("This Cancel action will close the "+screen+" Details form. \nYou will lose any changes you have made.\n Do you wish to continue?"))
window.close();
} else {
window.close();
}
}
function changeTitle(screen) {
this.focus();
if(document.forms[0].mode && document.forms[0].mode.value=="Edit") {
document.title="Edit "+screen;
} else {
document.title="Create "+screen;
}
checkRights();
if(document.forms[0].result && document.forms[0].result.value == "Y" && document.forms[0].tan.value != "Add" && document.forms[0].tan.value != "Reset")
refreshParent();
}
function checkRights() {
if(document.forms[0].read && document.forms[0].read.value=="Y") {
	for(i=0;i<document.forms[0].elements.length;i++) {
			document.forms[0].elements[i].disabled=true;

	}
	document.forms[0].cancel.disabled=false;
}
}
function resetDetails() {
if(isChanged() || (document.forms[0].result.value && document.forms[0].result.value=="N")) {
if(confirm("Reset action will reset all form data to that in the database. \nYou will lose any changes that you have made. \nDo you wish to continue?")) {
if(document.forms[0].mode.value == "Edit") {
document.forms[0].tan.value="E";
} else {
document.forms[0].tan.value="Reset";
}
document.forms[0].submit();
}
}
}
function resetScreen() {
if(isChanged() || (document.forms[0].result.value && document.forms[0].result.value=="N")) {
if(confirm("Reset action will reset all form data to that in the database. \nYou will lose any changes that you have made. \nDo you wish to continue?")) {
if(document.forms[0].mode.value != "Edit") {
document.forms[0].mode.value="I";
} 
document.forms[0].tan.value="Reset";
document.forms[0].submit();
}
}
}

function go(i) {
document.forms[0].target="main";
document.forms[0].start.value=i;
parent.frames[0].document.forms[0].start.value=i;
parent.frames[0].document.forms[0].total.value=document.forms[0].total.value;
document.forms[0].mode.value="R";
document.forms[0].submit();
}

function deselect(name) {
var count = 0;
var len = eval("document.forms[0]."+name+".length");
var component = eval("document.forms[0]."+name);
for(i=0;i<len;i++) {
if(component.options[i].selected) {
count++;
}
}
if(count > 1)
component.options[0].selected=false;
}
var fleetArr;
function makeFleetArray() {
var l = document.forms[0].hidFleet.options.length;
fleetArr = new Array(l);
for(i=0;i<l;i++) {
fleetArr[i] = document.forms[0].hidFleet.options[i].value;
}
}
var rankArr;
function makeRankArray() {
var l = document.forms[0].hidRank.options.length;
rankArr = new Array(l);
for(i=0;i<l;i++) {
rankArr[i] = document.forms[0].hidRank.options[i].value;
}
}
var DELIMITER = String.fromCharCode(164);
function filterRankCodes(nm,rankField) {
var rankCombo = eval("document.forms[0]."+rankField);
if(rankCombo.options) {
var selVal = nm.options[nm.selectedIndex].text;
if(selVal.length==0) {
makeRankArray();
var rnkCode;
rankCombo.options.length=0;
for(k=0;k<rankArr.length;k++) {
rnkCode = rankArr[k].split(DELIMITER);
rankCombo.options[k]=new Option(rnkCode[0],rnkCode[0]);
}
} else {
makeFleetArray();
var code;
var crewType;
for(i=0;i<fleetArr.length;i++) {
code = fleetArr[i].split(DELIMITER);
if(selVal==code[0]) {
crewType = code[1];
break;
}
}
makeRankArray();
var c=0;
var rCode;
rankCombo.options.length=0;
for(j=0;j<rankArr.length;j++) {
rCode = rankArr[j].split(DELIMITER);
if(crewType==rCode[1]) {
rankCombo.options[c]=new Option(rCode[0],rCode[0]);
c++;
}
}
}
}
}
function populateDescField(select,display){
	var desc = eval('document.forms[0].'+display);
	desc.value = select.value;
}
/* This function is for adding rows to a block
 * noOfRows -  no of rows to be added
 * rowContent -  HTML code for the row
 * divObj - reference to add row
 */
function addRow(noOfRows, rowContent, divObj) {
   for(var i=0; i<noOfRows;i++){
	   divObj.insertAdjacentHTML("BeforeEnd",rowContent);
   }
}

function addLoadEvent(func) {
	  var oldonload = window.onload;
	  if (typeof window.onload != 'function') {
	    window.onload = func;
	  } else {
	    window.onload = function() {
	      if (oldonload) {
	        oldonload();
	      }
	      func();
	    }
	  }
}

/*
 * The windowClose function is invoked when main window is unloaded
 * by using position of mouse click we will determine whether it is a 
 * browser close. If yes, we will re-direct the page to invoke loginPreAction.java
 * 
 */
function windowClose(contextName) {
		var iX = window.event.clientX ;
		var iY = window.event.clientY ;
		var ieVersion = 0;
		if (/MSIE (\d+\.\d+);/.test(navigator.userAgent)){ 
			  ieVersion=new Number(RegExp.$1);
		}
		if(ieVersion > 6 ) {
			//alert("IE version > 6" + "X component = " +iX + "  Y component = " + iY + "  iX >0 && iY< 0 = " + (iX >0 && iY< 0) );
			if (iX >0 && iY< 0  ) {
				if(contextName == undefined){
					//alert("contextName is undefined");
					window.parent.location.href='/mlt/endpreaction.do'
				} else {
					//alert(contextName);
					window.parent.location.href='/' + contextName + '/endpreaction.do'
				}
				
			}	 
		} else {
			//alert("IE version <= 6" + "X component = " +iX + "  Y component = " + iY + "  iX <(-5000) && iY < (-5000) && window.screenTop>10000 = " + (iX <(-5000) && iY < (-5000) && window.screenTop>10000) );
			if (iX <(-5000) && iY < (-5000) && window.screenTop>10000 ) {
				if(contextName == undefined){
					//alert("contextName is undefined");
					window.parent.location.href='/mlt/endpreaction.do'
				} else {
					//alert(contextName);
					window.parent.location.href='/' + contextName + '/endpreaction.do'
				}
			}
		}
}

function trapKeyboardEvents(contextName)
{
	document.onkeydown = function(){ checkKeycode(event,contextName); }
	
}
function checkKeycode(e,contextName) {
	
	e = e || event
	var keyChar = getChar(e)
		if((keyChar == "s+alt") || (keyChar == "W+ctrl")) {
			window.parent.location.href='/' + contextName + '/endpreaction.do'
		}
}
//event.type must be keypress/keydown/keyup
function getChar(event) {
  if (event.which == null) {
    return String.fromCharCode(event.keyCode)+ (event.shiftKey ? "+shift" : "") +(event.ctrlKey ? "+ctrl" : "") + (event.altKey ? "+alt" : "") + (event.metaKey ? "+meta" : "") ;// for IE
  } else if (event.which!=0 && event.charCode!=0) {
    return String.fromCharCode(event.which) + (event.shiftKey ? "+shift" : "") +(event.ctrlKey ? "+ctrl" : "") + (event.altKey ? "+alt" : "") + (event.metaKey ? "+meta" : "") ; ;  // the rest
  } else {
    return  null ;// special key
  }
}

