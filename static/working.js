var secretpassword = ""
function createPassword(selectedform)
{
    if (secretpassword.length < 3)
    {
        alert('Atleast 2 images must be selected.');
    }
    else
    {
        const passwordField = document.createElement("input");
        passwordField.type = 'hidden';
        passwordField.name = 'password';
        passwordField.value = secretpassword;
        selectedform.appendChild(passwordField);
        return true;
    }
}
function getPasswordType(selectedtype)
{
    let passwordtype = String(selectedtype.value);
    secretpassword = passwordtype;
    document.getElementById('x').style.display = 'none';
    document.getElementById('y').style.display = 'none';
    document.getElementById('z').style.display = 'none';
    document.getElementById(passwordtype).style.display = 'inline-block';
    for (let temp=97; temp<123; temp++)
    {
        let idname = passwordtype.concat(String.fromCharCode(temp));
        document.getElementById(idname).style.background = 'transparent';
    }
}
function imageClick(selectedimage)
{
    var oldinput = secretpassword;
    var newinput = "";
    if (oldinput.charAt(oldinput.length-1) == selectedimage.id.charAt(1))
    {
        newinput = oldinput.slice(0, -1);
        secretpassword = newinput;
        document.getElementById(selectedimage.id).style.backgroundColor = "transparent";
    }
    else
    {
        if (!oldinput.includes(selectedimage.id.charAt(1)))
        {
            newinput = oldinput.concat(selectedimage.id.charAt(1));
            secretpassword = newinput;
            document.getElementById(selectedimage.id).style.backgroundColor = "red";
            document.getElementById(selectedimage.id).style.borderRadius = "10%";
        }
    }
}