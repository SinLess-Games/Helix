import {useContext} from 'react';
import {GuildContext} from "../utils/contexts/GuildContext";

export const CategoryPage = () => {
    const {guildId} = useContext(GuildContext)
    return <div>Category Page {guildId}</div>
};