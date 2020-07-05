const express = require('express');
const cors = require('cors');
const {nanoid} = require('nanoid');
const monk = require('monk');
const yup = require('yup');

const app = express();
const url = 'localhost:27017/urlShortener';
const db = monk(url);
const urls = db.get('urls');
urls.createIndex({ url: 1 }, { unique: true })

db.then(() => {
    console.log('Connected correctly to server');
});

app.use(express.static('./public'));
app.use(express.json());
app.use(cors());

const schema = yup.object().shape({
    url: yup.string().url().trim().required(),
});

app.post('/url', (req, res) => {
    const {url} = req.body;
    const slug = nanoid(5);
    console.log(`In index.js: ${slug}`);
    console.log(`In index.js: ${url}`);
    schema.validate({url})
        .then( async (data) => {
            const urlFound = await urls.findOne(data);
            if (urlFound){
                console.log(`${url} is already existed`);
                res.json({
                    url: urlFound.url,
                    slug: urlFound.slug
                })
            }else{
                urls.insert({url: data.url, slug: slug});
                res.json({
                    url: data.url,
                    slug: slug
                })
            }
        })
        .catch( (err) => {
            res.status(500);
            res.json({
                message: `The url is invalid. Please try again`
            });
        })
});

app.get('/:id', async (req, res) => {
    const {id: slug} = req.params;
    const urlFound = await urls.findOne({slug});
    if (urlFound){
        res.redirect(urlFound.url);
    }
});

app.listen(3000, (err) => {
    if (err){
        res.json({
            message: err  
        });
    }
});