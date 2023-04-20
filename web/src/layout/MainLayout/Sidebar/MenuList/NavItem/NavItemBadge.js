import * as React from 'react';
import styled from 'styled-components';

const BadgeContainer = styled.div`
    margin-top: 4px;
    margin-bottom: 4px;
`;

const BadgeContent = styled.div`
    display: flex;
    flex-flow: row wrap;
    -webkit-box-pack: center;
    place-content: center;
    -webkit-box-align: center;
    align-items: center;
    box-sizing: border-box;
    font-weight: 500;
    font-size: 0.75rem;
    min-width: 20px;
    line-height: 1;
    padding: 0px 6px;
    height: 20px;
    border-radius: 10px;
    z-index: 1;
    transition: transform 225ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;
    // background-color: rgb(156, 39, 176);
    // color: rgb(255, 255, 255);
    ${({ active }) =>
        active &&
        `
            background-color: rgb(156, 39, 176);
            color: rgb(255, 255, 255);
    `}
    ${({ active }) =>
        !active &&
        `
            background-color: #ede7f6;
            color: inherit;
    `}
    transform-origin: 100% 0%;
`;

const NavItemBadge = ({ content, active }) => {
    return (
        <React.Fragment>
            <BadgeContainer>
                <BadgeContent active={active}>{content}</BadgeContent>
            </BadgeContainer>
        </React.Fragment>
    );
};

export default NavItemBadge;
