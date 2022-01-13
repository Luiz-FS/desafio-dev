import React from "react";
import { useHistory } from 'react-router-dom';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import PropTypes from 'prop-types';

const NavigationListItem = props => {
    const {
        title,
        icon: Icon,
        href
    } = props;

    const history = useHistory();

    const handleOnClick = () => {
        history.push(href);
    }

    return (
        <ListItem button onClick={handleOnClick}>
            <ListItemIcon>
                {Icon && <Icon/>}
            </ListItemIcon>
            <ListItemText primary={title} />
        </ListItem>
    );
}


NavigationListItem.propTypes = {
    title: PropTypes.string,
    icon: PropTypes.any,
    href: PropTypes.string
};

export default NavigationListItem;
