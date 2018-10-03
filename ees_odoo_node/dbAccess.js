/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */


async function dbAccess(){
    
    var conString = "postgress://openpg:openpgpwd@localhost:5432/eesti_restaurant";
    const {Client} = require('pg');
    const client = new Client(conString);

    await client.connect();

    const res = await client.query('SELECT $1::text as message', ['Hello world!']);
    console.log(res.rows[0].message); // Hello world!
    await client.end();
}

dbAccess()
  .then(console.log)
  .catch(console.error)