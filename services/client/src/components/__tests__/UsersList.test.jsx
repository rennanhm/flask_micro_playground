import React from 'react';
import renderer from 'react-test-renderer';
import {shallow} from 'enzyme';

import UsersList from '../UsersList';

const users = [
    {
        'active': true,
        'email': 'rennan@almeida.com',
        'id': 1,
        'username': 'rennan'
    },
    {
        'active': true,
        'email': 'paulo@teste.com',
        'id': 2,
        'username': 'paulo'
    }
];

test('UsersList renders properly', () => {
    const wrapper = shallow(<UsersList users={users}/>);
    const element = wrapper.find('h4');
    expect(element.length).toBe(2);
    expect(element.get(0).props.children).toBe('rennan');
});

test('UsersList renders a snapshot properly', () => {
    const tree = renderer.create(<UsersList users={users}/>).toJSON();
    expect(tree).toMatchSnapshot();
});
