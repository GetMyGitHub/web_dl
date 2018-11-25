

var selected_group
var selected_node_from_nodes_list
var selected_node_from

var old_selected_group;
function select_group(id, name) {
    selected_group = name;
    if (document.getElementById(old_selected_group)) {
        document.getElementById(old_selected_group).style.color = "black";
    }
    old_selected_group = id;
    document.getElementById("test").innerHTML =
     name + " selected";
    document.getElementById(id).style.color = "red";
    sessionStorage.setItem('selected_group', name);

}

var old_selected_node_from_nodes_list;
function select_node(id, name) {
  selected_node_from_nodes_list = name;
    if (document.getElementById(old_selected_node_from_nodes_list)) {
        document.getElementById(old_selected_node_from_nodes_list).style.color = "black";
    }
    old_selected_node_from_nodes_list = id;
    document.getElementById("test").innerHTML =
     name + " selected";
    document.getElementById(id).style.color = "red";
}

function add_node_in_group(){
   if (selected_group != null && selected_node_from_nodes_list != null) {
     callAjax("/nodes_groups/add_node/" + selected_group + "/" + selected_node_from_nodes_list);
   }
}


function callAjax(request) {
   var xhttp;
   if (window.XMLHttpRequest) {
     // code for modern browsers
     xhttp = new XMLHttpRequest();
     } else {
     // code for IE6, IE5
     xhttp = new ActiveXObject("Microsoft.XMLHTTP");
   }
   xhttp.onreadystatechange = function() {
     if (this.readyState == 4 && this.status == 200) {
       var response = this.responseText;
       self.location.href="/nodes_groups/";
     }
   };
   xhttp.open("GET", request, true);
   xhttp.send();
 }
