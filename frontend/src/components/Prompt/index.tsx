import { ReactNode } from 'react';
import cx from 'classnames';
import './styles.scss';

type PromptProps = {
    content: string;
    author: {
        name: string;
        avatar: string;
    };
    type: 'Text' | 'PDF'; 
    fileURL?: string; 
    children?: ReactNode;
}

export function Prompt({
    content,
    author,
    type,
    fileURL,
    children
}: PromptProps){

    const isPDF = type === 'PDF';
    
    const contentElement = isPDF && fileURL ? (
        // if type = "PDF", have link
        <a 
            href={fileURL} 
            target="_blank"
            rel="noopener noreferrer" 
            className="pdf-link" 
        >
            🔗 {content}
        </a>
    ) : (
        // if type = "Text", dont have link
        <p>{content}</p>
    );

    return (
        <div 
            className={cx(
            'prompt', 
            { 'pdf-prompt': isPDF } 
            )}
        >
            {contentElement} 
            
            <footer>
                <div className="user-info">
                    <img src={author.avatar} alt={author.name} />
                    <span>{author.name}</span>
                </div>
                <div>{children}</div>
            </footer>
        </div>
    );
}