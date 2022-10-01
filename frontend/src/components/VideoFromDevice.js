import {Container, Table} from "react-bootstrap";


export default function VideoFromDevice() {

    // получить лист

    let list_videos = [ {"src": "vid1.mp4", "name": "some name1"}, {"src": "vid2.mp4", "name": "some name2"}, {"src": "vid2.mp4", "name": "some name"}]
    let video_arr = []

    for (let vid in list_videos){
        if (vid % 2 === 0){
            if (vid != list_videos.length - 1){
                video_arr.push( <tr key={list_videos[vid]["name"]}><td><video src={list_videos[vid]["src"]} controls width="90%">
                </video></td><td><video src={list_videos[vid]["src"]} controls width="90%">
                </video></td></tr>)
            }else{
                video_arr.push( <tr key={list_videos[vid]["name"]}><video src={list_videos[vid]["src"]} controls width="90%">
                </video></tr>)
            }
        }

    }


    return (
        <Container>
            <Table>
                <tbody>
                {video_arr}
                </tbody>

            </Table>
        </Container>
    );
}
