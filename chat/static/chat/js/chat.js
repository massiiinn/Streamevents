// chat.js - VERSIÓ COMPLETA AMB PERMISOS VISIBLES

// =================== VARIABLES GLOBALS ===================
let eventId; // ID de l'esdeveniment actual
let currentUser = ''; // Nom d'usuari de la persona que està navegant

// =================== INICIALITZACIÓ ===================
// Quan el DOM estigui completament carregat
document.addEventListener('DOMContentLoaded', function() {
    // Obtenir l'ID de l'esdeveniment del data-attribute
    eventId = document.querySelector('.chat-container')?.dataset.eventId;
    // Obtenir el nom de l'usuari actual
    currentUser = document.querySelector('[data-username]')?.dataset.username || '';
    
    // Comprovar que tenim l'eventId
    if (!eventId) {
        console.error('No se encontró eventId');
        return;
    }
    
    console.log('Usuario actual:', currentUser);
    
    // =================== CONFIGURAR EVENTS ===================
    // Event listener per enviar missatges
    const chatForm = document.getElementById('chat-form');
    if (chatForm) {
        chatForm.addEventListener('submit', sendMessage);
    }
    
    // Delegació d'esdeveniments per eliminar missatges
    // Escoltem clics a tot el document i comprovem si s'ha clicat el botó d'eliminar
    document.addEventListener('click', function(e) {
        if (e.target.closest('.delete-message')) {
            const messageDiv = e.target.closest('.chat-message');
            if (messageDiv) {
                const messageId = messageDiv.dataset.messageId;
                if (messageId) {
                    deleteMessage(messageId);
                }
            }
        }
    });
    
    // Carregar els missatges inicials
    loadMessages();
    
    // Polling: recarregar missatges cada 3 segons per simular temps real
    setInterval(loadMessages, 3000);
});

// =================== CARREGAR MISSATGES ===================
// Fa una petició al servidor per obtenir tots els missatges de l'esdeveniment
function loadMessages() {
    if (!eventId) return;
    
    fetch(`/chat/${eventId}/messages/`)
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('chat-messages');
            const countElement = document.getElementById('message-count');
            
            if (!container) return;
            
            // Netejar el contenidor abans d'afegir els missatges
            container.innerHTML = '';
            
            if (data.messages && data.messages.length > 0) {
                // Crear l'HTML de cada missatge i afegir-lo al contenidor
                data.messages.forEach(msg => {
                    container.appendChild(createMessageElement(msg));
                });
                
                // Actualitzar el comptador de missatges al badge
                if (countElement) {
                    countElement.textContent = data.messages.length;
                }
            } else {
                // Si no hi ha missatges, mostrar un text informatiu
                container.innerHTML = '<p class="text-muted text-center">No hi ha missatges encara</p>';
                if (countElement) {
                    countElement.textContent = '0';
                }
            }
            
            // Fer scroll automàtic fins al final
            scrollToBottom();
        })
        .catch(error => {
            console.error('Error cargando mensajes:', error);
        });
}

// =================== ENVIAR MISSATGE ===================
// Envia un nou missatge al servidor quan l'usuari fa submit al formulari
function sendMessage(e) {
    e.preventDefault(); // Prevenir el comportament per defecte del formulari
    
    const form = e.target;
    const textarea = form.querySelector('textarea[name="message"]');
    const button = form.querySelector('button[type="submit"]');
    const errorsContainer = document.getElementById('chat-errors');
    
    // Validació: el missatge no pot estar buit
    if (!textarea.value.trim()) {
        if (errorsContainer) {
            errorsContainer.innerHTML = '<div class="alert alert-danger">El missatge no pot estar buit</div>';
        }
        return;
    }
    
    // Netejar errors anteriors
    if (errorsContainer) errorsContainer.innerHTML = '';
    
    // Deshabilitar el botó mentre s'envia (feedback visual)
    const originalText = button.textContent;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>'; // Spinner d'enviament
    button.disabled = true;
    
    // Enviar el missatge al servidor via POST
    fetch(`/chat/${eventId}/send/`, {
        method: 'POST',
        body: new FormData(form) // Inclou CSRF token i missatge
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Si s'ha enviat correctament: netejar el textarea
            textarea.value = '';
            
            // Recarregar els missatges per mostrar el nou
            loadMessages();
        } else {
            // Si hi ha errors (validacions, paraules prohibides, etc.)
            if (errorsContainer) {
                let errorHtml = '<div class="alert alert-danger">';
                if (data.errors) {
                    // Errors del formulari (validacions de Django)
                    Object.values(data.errors).flat().forEach(err => {
                        errorHtml += `<div>${escapeHtml(err)}</div>`;
                    });
                } else if (data.error) {
                    // Error general (esdeveniment no en directe, etc.)
                    errorHtml += `<div>${escapeHtml(data.error)}</div>`;
                }
                errorHtml += '</div>';
                errorsContainer.innerHTML = errorHtml;
            }
        }
    })
    .catch(error => {
        console.error('Error enviando mensaje:', error);
        if (errorsContainer) {
            errorsContainer.innerHTML = '<div class="alert alert-danger">Error de connexió</div>';
        }
    })
    .finally(() => {
        // Restaurar el botó al seu estat original
        button.textContent = originalText;
        button.disabled = false;
    });
}

// =================== CREAR ELEMENT HTML DE MISSATGE ===================
// Genera l'HTML d'un missatge individual amb tots els seus components
function createMessageElement(msg) {
    const isCurrentUser = msg.user === currentUser; // Comprova si és el nostre missatge
    const div = document.createElement('div');
    
    // Cada usuari té un color únic generat a partir del seu username
    const userColor = stringToColor(msg.user);
    
    div.className = `chat-message mb-3 p-3 rounded`;
    div.style.borderLeft = `5px solid ${userColor}`; // Barra lateral de color
    div.dataset.messageId = msg.id;

    // Si el missatge està destacat pel creador de l'esdeveniment
    if (msg.is_highlighted) {
        div.classList.add('highlighted');
    }

    // =================== BOTÓ D'ELIMINAR ===================
    let deleteButton = '';
    if (msg.can_delete === true) {
        // Text diferent si elimines el teu missatge o un d'altre (admin)
        const buttonText = isCurrentUser ? 'Eliminar' : 'Eliminar (Admin)';
        const buttonClass = isCurrentUser ? 'btn-outline-danger' : 'btn-outline-warning';
        deleteButton = `
            <div class="message-actions text-end mt-2">
                <button class="delete-message btn btn-sm ${buttonClass}" 
                        title="${isCurrentUser ? 'Eliminar tu mensaje' : 'Eliminar como administrador'}">
                    <i class="fas fa-trash"></i> ${buttonText}
                </button>
            </div>`;
    }

    // Badge "Admin" si l'usuari actual pot eliminar missatges d'altres
    const adminBadge = msg.can_delete && !isCurrentUser ? 
        '<span class="badge bg-warning text-dark ms-2"><i class="fas fa-shield-alt"></i> Admin</span>' : '';

    // =================== HTML FINAL DEL MISSATGE ===================
    div.innerHTML = `
        <div class="message-header d-flex justify-content-between align-items-start mb-2">
            <div>
                <strong style="color:${userColor}">${escapeHtml(msg.display_name)}</strong>
                ${adminBadge}
                <small class="text-muted ms-2">@${escapeHtml(msg.user)}</small>
            </div>
            <small class="text-muted">${escapeHtml(msg.created_at)}</small>
        </div>
        <div class="message-content">
            <p class="mb-0">${escapeHtml(msg.message)}</p>
        </div>
        ${deleteButton}
    `;
    return div;
}

// =================== GENERAR COLOR ÚNIC PER USUARI ===================
// Converteix el nom d'usuari en un color hexadecimal únic i consistent
function stringToColor(str) {
    let hash = 0;
    // Calcular un hash numeric del string
    for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    // Convertir el hash a color hexadecimal
    const c = (hash & 0x00FFFFFF)
        .toString(16)
        .toUpperCase();
    return '#' + '00000'.substring(0, 6 - c.length) + c;
}


// =================== ELIMINAR MISSATGE ===================
// Marca un missatge com a eliminat (soft delete)
function deleteMessage(messageId) {
    // Confirmació abans d'eliminar
    if (!confirm('Segur que vols eliminar aquest missatge?\nAquesta acció no es pot desfer.')) {
        return;
    }
    
    // Obtenir el CSRF token per seguretat
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    
    // Enviar petició d'eliminació al servidor
    fetch(`/chat/message/${messageId}/delete/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/x-www-form-urlencoded',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Recarregar missatges per amagar l'eliminat
            loadMessages();
            showNotification('✅ Missatge eliminat correctament', 'success');
        } else {
            alert('Error: ' + (data.error || 'No tens permisos'));
        }
    })
    .catch(error => {
        console.error('Error eliminando mensaje:', error);
        alert('Error de connexió');
    });
}

// =================== SCROLL AUTOMÀTIC ===================
// Fa scroll fins al final del contenidor de missatges
function scrollToBottom() {
    const container = document.getElementById('chat-messages');
    if (container) {
        container.scrollTop = container.scrollHeight;
    }
}

// =================== NOTIFICACIÓ TEMPORAL ===================
// Mostra una alerta temporal a la cantonada superior dreta
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-eliminar després de 3 segons
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// =================== ESCAPAR HTML (SEGURETAT XSS) ===================
// Converteix caràcters especials en entitats HTML per prevenir injeccions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}