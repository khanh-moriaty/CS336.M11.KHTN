import {
    Typography,
    Card,
    CardMedia,
    CardContent,
    CardActionArea,
} from '@material-ui/core';

export default function Message(props) {

    return (
        <Card style={{display: 'flex', flexGrow: "1"}}>
            <CardActionArea style={{display: 'flex', flexDirection: "column"}}>
                <CardMedia
                    component="img"
                    // height="120"
                    style={{objectFit: 'fill'}}
                    image={props.image}
                />
                <CardContent style={{display: 'flex', flexDirection: "column", flex: '1'}}>
                    <Typography variant="caption2" color="text.secondary">
                        {props.title}
                    </Typography>
                </CardContent>
            </CardActionArea>
        </Card>
    )
        ;

}