import styled from 'styled-components';

import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import DockItem from './DockItem';

const DockContainer = styled.div`
    visibility: hidden;
    position: fixed;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    z-index: 999;
`;

const DockWrapperWidth = styled.div`
    padding: 0 25px;
`;

const DockWrapperHeight = styled.div`
    height: 100%;
`;

const DockWrapper = styled.div`
    float: right;
`;

export const Dock = ({ open, onClose, items }) => {
    const [_window, _setWindow] = useState({ width: 0, height: 0 });

    const _resize = () => {
        const ih = window.innerHeight;
        const iw = window.innerWidth;
        _setWindow({ width: iw, height: ih });
    };
    useEffect(() => {
        _resize();

        window.addEventListener('resize', _resize);

        return () => {
            window.removeEventListener('resize', _resize);
        };
    }, []);

    return (
        <DockContainer>
            <div>
                <DockWrapperWidth style={{ width: `${_window.width}px` }}>
                    <DockWrapperHeight style={{ height: `${_window.height}px` }}>
                        <DockWrapper>
                            {items
                                ? items.map((item) => (
                                      <DockItem
                                          key={item.id}
                                          id={item.id}
                                          title={item.title}
                                          state={item.state}
                                          onChangeState={item.onChangeState}
                                          toolbarChildren={item.toolbarChildren}
                                          onClose={() => {
                                              onClose(item);
                                          }}
                                      >
                                          {item.content}
                                      </DockItem>
                                  ))
                                : null}
                        </DockWrapper>
                    </DockWrapperHeight>
                </DockWrapperWidth>
            </div>
        </DockContainer>
    );
};

Dock.propTypes = {
    onClose: PropTypes.func.isRequired
};
