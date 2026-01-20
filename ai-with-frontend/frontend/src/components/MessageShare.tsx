import '../styles/message-share.scss';
import emptyChatImg from '../assets/images/empty-chat.svg'

type Props = {
    admin?: boolean;
}

export function MessageShare(props: Props){
    return (
       <div className="message-share">
        <img src={emptyChatImg} alt="No Chat" />
        <span>No prompts yet...</span>
        {
            props.admin ? (
                <p>Send this room code to your friends and <br/> start summarizing!</p>
            ) : (
                <p>Log in and be the first to <br/> write a prompt</p>
            )
        }
        
    </div> 
    )
}