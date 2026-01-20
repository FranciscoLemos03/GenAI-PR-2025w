import { ReactNode } from 'react';
import cx from 'classnames';
import './styles.scss';

type PromptProps = {
  content: string;
  author: {
    name: string;
    avatar: string;
  };
  type: 'Text' | 'PDF' | 'AI' | 'AI_TYPING';
  fileURL?: string;
  children?: ReactNode;
};

export function Prompt({
  content,
  author,
  type,
  fileURL,
  children
}: PromptProps) {

  const isPDF = type === 'PDF';
  const isAI = type === 'AI' || type === 'AI_TYPING';

  let contentElement;

  // PDF = link
  if (isPDF && fileURL) {
    contentElement = (
      <a
        href={fileURL}
        target="_blank"
        rel="noopener noreferrer"
        className="pdf-link"
      >
        🔗 {content}
      </a>
    );
  }
  // AI or normal text = formatted text
  else {
    contentElement = (
      <p style={{ whiteSpace: 'pre-line' }}>
        {content}
      </p>
    );
  }

  return (
    <div
      className={cx('prompt', {
        'pdf-prompt': isPDF,
        'ai-prompt': isAI
      })}
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
