const express = require('express')
const cors = require('cors')
const mysql = require('mysql')
const app = express()

const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'nikit',
    database: 'clitinderdatabase',
    multipleStatements: true
})

const PORT = 3001;

app.use(cors());
app.use(express.json());
app.use(
    express.urlencoded({
      extended: true
    })
  )

db.connect();

app.get('/getall', (req, res) =>{
    db.query('SELECT * FROM cliusers',(err, result)=>{
        console.log(result)
        res.send(result)
    })
})

app.get('/colsdata', (req, res) =>{
    const {col_name} = req.body;
    let colsget = col_name.join(',')
    console.log(col_name)
    db.query(`SELECT ${colsget} FROM cliusers`, (err, result)=>{
        console.log(result)
        console.log(err)
        res.send(result)
    })
})


app.get('/get', (req, res) =>{
    const {username, password} = req.body;
    db.query('SELECT * FROM cliusers WHERE username=? AND password=?',[username, password], (err, result)=>{
        console.log(result)
        res.send(result)
    })
})

app.get('/datacol', (req, res) =>{
    console.log("request made")
    const {col_name, condition} = req.body;
    console.log(col_name, condition)
    db.query(`SELECT * FROM cliusers WHERE ${col_name}="${condition}"`, (err, result)=>{
        console.log(result)
        console.log(err)
        res.send(result)
    })
})

app.get('/specialget', (req, res)=>{
    const {colname, condition, colstoget} = req.body;
    let colsget = colstoget.join(',')
    console.log("special")
    db.query(`SELECT ${colsget} FROM cliusers WHERE ${colname}="${condition}"`, (err, result)=>{
        console.log(result)
        console.log(err)
        res.send(result)
    })
})

app.post('/customquery', (req, res)=>{
    const {query} = req.body;
    db.query(`${query}`, (err, result)=>{
        console.log(err)
        res.send(result)
    })
})

app.post('/login', (req, res)=>{
    const {username, password} = req.body;
    db.query('SELECT * FROM cliusers WHERE username=? AND password=?',[username, password], (err, result)=>{
        console.log(result)
        res.send(result)
    })
})

app.post('/registerc', (req, res) =>{
    console.log(req.body)
    console.log("registered new")
    const {username, password, name, gender, emailid, code} = req.body;
    // console.log(username)
    db.query(`INSERT INTO cliusers (username, password, name, code, gender, emailid, likesyou, matches ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,[username, password, name, code, gender, emailid, '[]', '[]'], (err)=>{
        console.log(err)
    });
    res.send('OK')
})


app.get('/paticularcolsdatac', (req, res) =>{
    const {col_name} = req.body;
    console.log((col_name))
    db.query(`SELECT ${col_name} FROM cliusers`, (err, result)=>{
        console.log(result)
        console.log(err)
        res.send(result)
    })
})

app.post('/loginc', (req, res)=>{
    const {username, password} = req.body;
    db.query('SELECT * FROM cliusers WHERE username=? AND password=?',[username, password], (err, result)=>{
        console.log(result)
        res.send(result)
    })
})


app.get('/', (req, res)=>{
    res.send('Server is running')
})

app.listen(process.env.PORT || PORT, () => {
    console.log("Good to go boi")
})