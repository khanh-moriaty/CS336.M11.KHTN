import React from 'react';
import { makeStyles } from '@material-ui/core/styles';

import Pagination from '@material-ui/lab/Pagination';
import Button from '@material-ui/core/Button';

import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';

import { Container, Grid, Typography } from '@material-ui/core';

import { FormControl, TextField } from '@material-ui/core';

import Product from './Product';

const useStyles = makeStyles((theme) => ({
    root: {
        margin: theme.spacing(1),
    },
    card: {
        margin: '30pt 20pt 30pt 20pt',
        boxShadow: '5px 10px 20px 5px rgba(0, 0, 0, 0.5)'
    },
    media: {
        width: '100%',
    },
    pagination: {
        marginTop: theme.spacing(2),
    },
    formControl: {
        margin: theme.spacing(1),
        minWidth: 120,
    },
    container: {
        display: 'flex',
        flexWrap: 'wrap',
    },
    formButtom: {
        marginTop: '0.5em',
    }
}));

export default function Gallery(props) {

    const classes = useStyles();

    const pageCount = Math.ceil(props.imgList.length / props.imgPerPage);

    const topPagination = React.useRef();

    const updateCurrentPage = () => {
        const startIdx = (props.page - 1) * props.imgPerPage;
        const endIdx = Math.min(props.imgList.length, props.page * props.imgPerPage);
        const newList = props.imgList.slice(startIdx, endIdx);
        props.setCurrentPage(newList.map(img =>
            <Product
                image={img.image}
                title={img.title}
            />
        ));
        // topPagination.current.scrollIntoView();
    };

    const updatePage = x => {
        props.setPage(x);
    }

    React.useEffect(() => {
        updateCurrentPage(props.page);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [props.imgList, props.page]);

    const [dialogOpen, setDialogOpen] = React.useState(false);
    const [dialogPage, setDialogPage] = React.useState(0);

    const handleClickDialogOpen = () => {
        setDialogOpen(true);
    };

    const handleDialogClose = () => {
        setDialogOpen(false);
    };

    const handleConfirmDialog = () => {
        handleDialogClose();
        if (isNaN(dialogPage)) return;
        const page = Number(dialogPage);
        if (1 <= page && page <= pageCount)
            updatePage(page);
        else
            setDialogPage(props.page);
    }

    React.useEffect(() => {
        setDialogPage(props.page);
    }, [props.page])

    return (
        <Container style={{ padding: "0px 50px" }}>
            <Pagination
                className={classes.pagination}
                ref={topPagination}
                count={pageCount}
                style={{ display: "flex", justifyContent: "center" }}
                page={props.page} onChange={(e, x) => updatePage(x)}
                color="primary" size="small"
                showFirstButton showLastButton
            />
            <Button className={classes.formButtom} onClick={handleClickDialogOpen} color="secondary">Jump to page</Button>
            <Dialog open={dialogOpen} onClose={handleDialogClose}>
                <DialogContent>
                    <form className={classes.container} onSubmit={e => { e.preventDefault(); handleConfirmDialog(); }}>
                        <FormControl className={classes.formControl}>
                            <TextField
                                autoFocus
                                color="secondary"
                                id="dialog-textfield"
                                label="Page" type="number"
                                value={dialogPage}
                                onChange={e => setDialogPage(e.target.value)}
                            />
                        </FormControl>
                    </form>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleDialogClose} color="default">
                        Cancel
                    </Button>
                    <Button onClick={handleConfirmDialog} color="secondary">
                        Ok
                    </Button>
                </DialogActions>
            </Dialog>
            <Grid container spacing={4} alignItems="stretch" style={{ margin: "20px 0px" }}>
                {props.currentPage.map((example) => (
                    <Grid item key={1} xs={6} sm={3} md={2} style={{ display: 'flex' }}>
                        {example}
                    </Grid>
                ))}
            </Grid>
            {/* <Gallery currentPage={props.currentPage} /> */}
            <Pagination
                className={classes.pagination}
                count={pageCount}
                style={{ display: "flex", justifyContent: "center" }}
                page={props.page} onChange={(e, x) => updatePage(x)}
                color="primary" size="small"
                showFirstButton showLastButton
            />
        </Container>
    );
}