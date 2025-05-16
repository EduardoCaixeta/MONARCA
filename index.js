require('dotenv').config();
const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');
const { Client, GatewayIntentBits } = require('discord.js');

const client = new Client({
  intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent]
});

// Pasta para salvar imagens
const saveFolder = path.join(__dirname, 'images');
if (!fs.existsSync(saveFolder)) {
  fs.mkdirSync(saveFolder);
}

// Quando o bot inicia
client.once('ready', () => {
  console.log(`Bot online como ${client.user.tag}`);
});

// Quando recebe mensagem
client.on('messageCreate', async (message) => {
  if (message.author.bot) return;

  const content = message.content.toLowerCase();

  // ======= GUERRA =======
  if (content === '!liberar guerra') {
    const channel = message.guild.channels.cache.find(c => c.name === '⚔guerra');
    if (!channel) return message.reply('Canal #guerra não encontrado.');

    await channel.permissionOverwrites.edit(message.guild.roles.everyone, {
      SendMessages: true
    });

    return message.reply('Canal #guerra foi **liberado** para todos os membros.');
  }

  if (content === '!fechar guerra') {
    const channel = message.guild.channels.cache.find(c => c.name === '⚔guerra');
    if (!channel) return message.reply('Canal #guerra não encontrado.');

    await channel.permissionOverwrites.edit(message.guild.roles.everyone, {
      SendMessages: false
    });

    return message.reply('Canal #guerra foi **fechado** para os membros.');
  }

  // ======= NÍVEL DE PODER =======
  const powerChannelName = '💪nível-de-poder';
  if (message.channel.name === powerChannelName) {
    const legenda = message.content.trim();

    if (!['1', '2', '3', '4'].includes(legenda)) {
      return message.reply('Legenda inválida. Use apenas um número de 1 a 4.');
    }

    const attachment = message.attachments.first();
    if (!attachment || !attachment.contentType.startsWith('image/')) {
      return message.reply('Envie uma imagem com a legenda (1 a 4).');
    }

    const date = new Date();
    const ddmmyyyy = date.toLocaleDateString('pt-BR').replace(/\//g, '-');
    let baseName = `${legenda}_${ddmmyyyy}`;
    let count = 1;
    let filename;

    do {
      filename = `${baseName}#${count}.png`;
      count++;
    } while (fs.existsSync(path.join(saveFolder, filename)));

    const res = await fetch(attachment.url);
    const buffer = await res.buffer();
    fs.writeFileSync(path.join(saveFolder, filename), buffer);

    return message.reply(`Imagem salva como **${filename}**.`);
  }
});

// Login com o token
client.login(process.env.DISCORD_TOKEN);
