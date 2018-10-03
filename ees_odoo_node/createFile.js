/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */


// include node fs module
var fs = require('fs');
 
// writeFile function with filename, content and callback function
fs.writeFile('eesti.txt', 'Learn Node FS module', function (err) {
  if (err) throw err;
  console.log('File is created successfully.');
}); 