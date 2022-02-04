import React from 'react';
import '@fontsource/roboto';
import './App.css';

import { makeStyles } from '@material-ui/core/styles';

import { ThemeProvider, createTheme, responsiveFontSizes } from '@material-ui/core/styles';
import {
    Typography,
    AppBar,
    Toolbar,
    CssBaseline,
    Box,
    Container,
    Link,
    Grid,
    Paper,
    TextField,
    FormGroup,
    FormControlLabel,
    Checkbox,
    FormLabel,
    RadioGroup,
    Radio,
    FormControl
} from '@material-ui/core';

import Product from './Product';
import Gallery from './Gallery';

const theme = responsiveFontSizes(createTheme({
    typography: {
        fontFamily: [
            'Open Sans',
        ].join(','),
    },
    palette: {
        primary: {
            main: '#ED6A5A',
        },
        secondary: {
            main: '#000000',
        },
    }
}));

const useStyles = makeStyles(theme => ({
    root: {
        height: '100vh',
        width: '100vw',
        padding: '1vh',
        boxSizing: 'border-box',
        // backgroundImage: 'url("bg_musicbot.jpg")',
        // backgroundPosition: 'center',
        // backgroundSize: 'cover',
        // backgroundRepeat: 'no-repeat',
    },
    logo: {
        height: "50px",
        margin: "10px 10px",
    },
    title: {
        height: "100%",
        margin: "0px 10px",
    }
}));

function Copyright() {
    return (
        <Typography variant="body1" color="text.secondary" align="center">
            {'Copyright © Khanh Ho '}
            {new Date().getFullYear()}
            {'.'}
        </Typography>
    );
}

export default function App() {

    const classes = useStyles();

    const [exampleList, setExampleList] = React.useState([])

    const [currentQuery, setCurrentQuery] = React.useState({
        'id': "",
        'image': "007fca8ce9a042f9e1656ce8f96ba19d.jpg",
        'title': "",
    })

    const handleFileInputChange = (e) => {
        const file = e.target.files[0];
        console.log(file);

        const formData = new FormData();
        formData.append('file', file);


        fetch('http://192.168.24.43:8080/v1/upload',
            {
                method: 'POST',
                body: formData,
            }
        )
            .then((response) => response.json())
            .then((result) => {
                console.log('Success:', result);
                setCurrentQuery({
                    'id': "",
                    'image': result['image'],
                    'title': currentQuery['title'],
                })
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }

    // When app starts, fetch example list
    React.useEffect(() => {

        fetch('http://192.168.24.43:8080/v1/examples?count=6')
            .then((response) => response.json())
            .then((result) => {
                console.log('Success:', result);
                setExampleList(result['results']);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }, [])

    React.useEffect(() => {
        console.log('Debug: ', exampleList);
    }, [exampleList])

    const [resultList, setResultList] = React.useState([]);
    const [processingTime, setProcessingTime] = React.useState(0);
    const [corpusSize, setCorpusSize] = React.useState(0);
    const [score, setScore] = React.useState("N/A");
    const [page, setPage] = React.useState(1);
    const [currentPage, setCurrentPage] = React.useState([]);
    const imgPerPage = 18;

    React.useEffect(() => {
        setPage(1);
    }, [resultList]);

    React.useEffect(() => {
        var fetchURL;
        if (currentQuery.id.length > 0)
            fetchURL = 'http://192.168.24.43:8080/v1/query?model_text=tfidf&id=' + currentQuery.id;
        else
            fetchURL = 'http://192.168.24.43:8080/v1/query?model_text=tfidf&title=' + currentQuery.title + '&image=' + currentQuery.image;

        fetch(fetchURL)
            .then((response) => response.json())
            .then((result) => {
                console.log('Success:', result);
                setResultList(result['results']);
                setProcessingTime(result['processing_time']);
                setCorpusSize(result['corpus_size']);
                setScore(result['score']);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }, [currentQuery])

    return (
        <div className="App">
            <ThemeProvider theme={theme}>
                <CssBaseline />
                <AppBar position="relative">
                    <Toolbar>
                        <img src="logo_shopee.png" alt="Shopee Logo" className={classes.logo} draggable="false" />
                        <Typography variant="h5" color="inherit" className={classes.title} noWrap>
                            Shopee Product Matching
                        </Typography>
                    </Toolbar>
                </AppBar>
                {/* Hero unit */}
                <Box
                    sx={{
                        bgcolor: 'background.paper',
                        pt: 8,
                        pb: 6,
                    }}
                >
                    <Container maxWidth="md">
                        <Typography
                            component="h1"
                            variant="h2"
                            align="center"
                            color="text.primary"
                            gutterBottom
                        >
                            Shopee Product Matching
                        </Typography>
                        <Typography variant="h6" align="center" color="text.secondary" paragraph>
                            Do you scan online retailers in search of the best deals? Query our product matching
                            system by inputing an image and its title, then we will retrieve similar items for you in no time!
                        </Typography>
                    </Container>

                    <Container maxWidth="md" style={{ marginTop: '40px' }}>
                        <Paper elevation={4} style={{ padding: '30px' }}>
                            <Grid container spacing={4} alignItems="center">
                                <Grid item xs={12} md={6}>
                                    <TextField
                                        label="Product title"
                                        value={currentQuery.title}
                                        onChange={(e) => {
                                            setCurrentQuery({
                                                'id': "",
                                                'image': currentQuery['image'],
                                                'title': e.target.value,
                                            })
                                        }}
                                        id="outlined-basic"
                                        variant="outlined"
                                        size="small"
                                    />
                                    <label htmlFor="contained-button-file">
                                        <img
                                            src={'http://192.168.24.43:8080/v1/img/' + currentQuery.image}
                                            alt="selected query"
                                            style={{
                                                margin: "10px",
                                                width: "260px",
                                                height: "260px",
                                            }}
                                        />
                                    </label>
                                    <input
                                        style={{ whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis", width: "250px" }}
                                        accept="image/*"
                                        className={classes.input}
                                        id="contained-button-file"
                                        type="file"
                                        onChange={handleFileInputChange}
                                    />
                                    <Container style={{ marginTop: '30px' }}>
                                        <Grid container spacing={4} alignItems="flex-start">
                                            <Grid item xs={6}>
                                                <FormControl>
                                                    <FormLabel id="radio-text-model">Text descriptor</FormLabel>
                                                    <RadioGroup
                                                        defaultValue="tfidf"
                                                        name="radio-text-model"
                                                    >
                                                        <FormControlLabel value="tfidf" control={<Radio color="primary" />} label="TF-IDF" />
                                                        <FormControlLabel value="bm25" control={<Radio color="primary" />} label="BM25" />
                                                        <FormControlLabel value="none" control={<Radio color="primary" />} label="None" />
                                                    </RadioGroup>
                                                </FormControl>
                                            </Grid>
                                            <Grid item xs={6}>
                                                <FormControl>
                                                    <FormLabel id="radio-image-model">Visual descriptor</FormLabel>
                                                    <RadioGroup
                                                        defaultValue="none"
                                                        name="radio-image-model"
                                                    >
                                                        <FormControlLabel value="phash" control={<Radio color="primary" />} label="pHash" />
                                                        <FormControlLabel value="sift" control={<Radio color="primary" />} label="SIFT" />
                                                        <FormControlLabel value="none" control={<Radio color="primary" />} label="None" />
                                                    </RadioGroup>
                                                </FormControl>
                                            </Grid>
                                            <Grid item xs={12}>
                                                <FormGroup>
                                                    <FormLabel id="radio-image-model">Other options</FormLabel>
                                                    <FormControlLabel control={<Checkbox color="primary" />} label="Text query expansion" />
                                                    <FormControlLabel control={<Checkbox color="primary" />} label="Visual query expansion" />
                                                </FormGroup>
                                            </Grid>
                                        </Grid>
                                    </Container>
                                </Grid>
                                <Grid item xs={12} md={6}>
                                    <Typography variant="h5" style={{ marginBottom: '10px' }}>...or try these examples:</Typography>
                                    <Grid container spacing={4} alignItems="stretch">
                                        {exampleList.map((example) => (
                                            <Grid item key={1} xs={6} sm={4} md={4} style={{ display: 'flex' }}>
                                                <Product
                                                    image={example.image}
                                                    title={example.title}
                                                    onClick={() => {
                                                        setCurrentQuery(example);
                                                    }}
                                                />
                                            </Grid>
                                        ))}
                                    </Grid>
                                </Grid>
                            </Grid>
                        </Paper>
                    </Container>

                    <Container style={{ marginTop: "50px" }}>
                        <Typography component="body1" variant="h6" align="center" color="text.secondary">
                            Found {resultList.length} / {corpusSize} results in {processingTime} seconds.
                        </Typography>
                        <Typography variant="body1" align="center" color="text.secondary">
                            AP score: {score}.
                        </Typography>
                        <Gallery
                            imgList={resultList} imgPerPage={imgPerPage}
                            setPage={setPage} setCurrentPage={setCurrentPage}
                            page={page} currentPage={currentPage}
                        />
                    </Container>
                </Box>
                {/* Footer */}
                <Box sx={{ bgcolor: 'background.paper', p: 6 }} component="footer">
                    <Container maxWidth="sm">
                        <Typography
                            variant="subtitle2"
                            align="center"
                            color="text.secondary"
                            component="p"
                            paragraph
                        >
                            {'This website is part of our final project for the CS336.M11.KHTN course.'} <br />
                            {'We would like to acknowledge the insightful lectures from Dr. Thanh Duc Ngo, along with '}
                            {'the Product Matching dataset from '}
                            <Link href="https://www.kaggle.com/c/shopee-product-matching/overview" target="_blank">
                                Shopee Kaggle Challenge.
                            </Link>
                        </Typography>
                        <Copyright />
                    </Container>
                </Box>
            </ThemeProvider>
        </div>
    );
}