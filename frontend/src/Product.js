import {
    Typography,
    Card,
    CardMedia,
    CardContent,
    CardActionArea,
} from '@material-ui/core';

import Image from 'material-ui-image';

export default function Message(props) {

    return (
        <Card style={{ display: 'flex', flexGrow: "1" }}>
            <CardActionArea style={{ display: 'flex', flexDirection: "column" }} onClick={props.onClick}>
                <CardMedia
                    // component="img"
                // height="120"
                // style={{ objectFit: 'fill' }}
                // image={'http://192.168.24.43:8080/v1/img/' + props.image}
                style={{width: "100%"}}
                >
                    <Image
                        src={'http://192.168.24.43:8080/v1/img/' + props.image}
                        // style={{ objectFit: 'fill' }}
                    />
                </CardMedia>
                <CardContent style={{ display: 'flex', flexDirection: "column", flex: '1' }}>
                    <Typography variant="caption2" color="text.secondary">
                        {props.title.slice(0, 32) + (props.title.length > 32 ? '...' : '')}
                    </Typography>
                </CardContent>
            </CardActionArea>
        </Card>
    );

}