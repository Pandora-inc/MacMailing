# MacMailling

Aplicación para la gestión y planificación de envíos de correos a clientes. Gestión de calendario de envíos y administración de los usuarios.

## Manual de usuario

Esta es una guía de uso de la aplicación orientada al usuario final y al administrador. Para obtener una gia técnica de implantación y mantenimiento diríjase al archivo README.md.

### Secciones

- [Pantalla de inicio](#pantalla-de-inicio)
- [Grupos](#grupos)
- [Usuarios](#usuarios)
- [Eventos](#eventos)
- [Accounts](#accounts)
- [Clientes](#clientes)
- [Clientes addresss](#clientes-addresss)
- [Clientes contacts](#clientes-contacts)
- [Clientes emails](#clientes-emails)
- [Clientes socials](#clientes-socials)
- [Clientes utms](#clientes-utms)
- [Clientes webs](#al-lado-del-bot%C3%B3n)
- [Contact types](#contact-types)
- [Countryss](#countryss)
- [Email types](#email-types)
- [Excel filess](#excel-filess)
- [Mail corps](#mail-corps)
- [Mails](#mails)
- [Mails to sends](#mails-to-sends)
- [Social types](#social-types)
- [Template filess](#template-filess)
- [Templates groups](#templates-groups)
- [Web types](#web-types)
- [Calendario](#calendario)

#### Pantalla de inicio

El acceso a esta es por medio de la direccion de administración del sitio [url del sitio]:8000/admin.

Ej. el acceso a el ambiente de pruebas seria por el siguiente [link](http://macmailling.eastus.cloudapp.azure.com:8000/admin/).

Al acceder lo primero que veremos seria la pantalla de inicio de sesión.

[![Iniciar sesión](img\00_iniciar_sesion.png "Iniciar sesión")](img\00_iniciar_sesion.png "Iniciar sesión")

Una vez ingresadas las credenciales proporcionadas por el administrados podremos acceder a la pantalla de inicio del sitio.

En la pantalla de inicio vemos un listado con las ultimas acciones que realizo el usuario y el menu con las opciones que tiene este autorizadas.

[![Pantalla de inicio](img\01.png "Pantalla de inicio")](img\01.png "Pantalla de inicio")

En la esquina superior derecha de la pantalla tenderemos un botón para cerrar la sección. De esta manera podremos salir del sistema. Al presionarlo nos cerrara la sesión y nos mostrara un mensaje por si queremos volver a iniciarla.

[![Cerrar sesión](img\00_cerrar_secion.png "Cerrar sesión")](img\00_cerrar_secion.png "Cerrar sesión")

Al lado del botón de cerrar sesión tenemos otro para cambiar la contraseña.

[![Cambiar password](img\00_cambiar_password.png "Cambiar password")](img\00_cambiar_password.png "Cambiar password")

Si todo sale bien, se mostrara un mensaje de confirmación del cambio de contraseña.

[![Cambiar password confirmación](img\00_cambiar_password_exito.png "Cambiar password confirmación")](img\00_cambiar_password_exito.png "Cambiar password confirmación")

Si se coloca mal la contraseña antigua se mostrara un mensaje de error y no permitirá el cambio.

[![Cambiar password error](img\00_cambiar_password_error.png "Cambiar password error")](img\00_cambiar_password_error.png "Cambiar password error")

- [Volver al indice](#secciones)

#### Grupos

Pantalla para la administración y creación de los grupos de usuarios. Estos son una forma de generar grupos de permisos de acceso a la aplicación. De esta forma se puede definir un conjunto de permisos y luego aplicarle los mismos a muchos usuarios distintos.

[![Permisos Grupos](img\02_grupo_permisos.png "Permisos Grupos")](img\02_grupo_permisos.png "Permisos Grupos")

##### Crear / Editar grupos

La pantalla de creación de grupos y de edición son la misma, la diferencia es que en la edición trae los datos del grupo que queremos modificar.

En esta pantalla podremos ponerle un nombre al grupo y seleccionar los permisos que tendrá cada persona.

[![Crear Permisos Grupos](img\02_grupo_crear.png "Crear Permisos Grupos")](img\02_grupo_crear.png "Crear Permisos Grupos")

Los permisos se asignan pasándolos de la pantalla de permisos disponibles a permisos seleccionados. Estos permisos se dividen en cuatro tipos:

- **Add**: *agregar un elemento.* Si no se da permisos de Add el usuario no vera el botón de nuevo en esa pantalla y no podrá agregar nuevos elementos.
- **Change**: *cambiar un elemento.* Si no se dan los permisos de change el usuario no podrá modificar los datos ya existentes.
- **Delete**: *eliminar un elemento.* Si no se dan permisos de delete no se podrán eliminar los elementos de los listados.
- **View**: *ver elementos.* Si no se dan permisos de view el usuario no vera ese elemento en el menu, ni podrá acceder al listado de estos.

[![Permisos Grupos](img\02_grupo_permisos.png "Permisos Grupos")](img\02_grupo_permisos.png "Permisos Grupos")

Luego de crear un grupo veremos un mensaje de confirmación y este aparecerá en el listado y en la lista de grupos para agregarles a los usuarios.

[![Confirmación creación Grupos](img\02_grupo_crear_confirmacion.png "Confirmación creación Grupos")](img\02_grupo_crear_confirmacion.png "Confirmación creación Grupos")

##### Eliminar grupos

Para eliminar un grupo se selecciona este tildándolo y en el menu de acciones seleccionar la opción *"Eliminar grupos seleccionados/as"* , luego presionar el botón Ejecutar.

[![Eliminar Grupos](img\02_grupo_eliminar.png "Eliminar Grupos")](img\02_grupo_eliminar.png "Eliminar Grupos")

Si esta todo correcto se pedirá la confirmación de la eliminación.

[![Confirmación eliminar Grupos](img\02_grupo_eliminar_confirmar.png "Confirmación eliminar Grupos")](img\02_grupo_eliminar_confirmar.png "Confirmación eliminar Grupos")

Luego de aceptar volveremos al listado y veremos la confirmación del borrad

Si un grupo llega a estar asociado a algún usuario ese usuario dejara de tenerlo en su listado de grupos asociados.

- [Volver al indice](#secciones)

#### Usuarios

En esta pantalla podemos crear y administrar los usuarios

##### Crear / Editar usuarios

La pantalla de creación de usuarios y de edición son la misma, la diferencia es que en la edición trae los datos del usuario que queremos modificar.

En esta pantalla podremos:

##### Eliminar usuarios

Para eliminar un usuario se selecciona este tildándolo y en el menu de acciones seleccionar la opción *"Eliminar usuarios seleccionados/as"* , luego presionar el botón Ejecutar.

Si esta todo correcto se pedirá la confirmación de la eliminación.

Luego de aceptar volveremos al listado y veremos la confirmación del borrado.

´´´ Si llega a haber un usuarios asociado nos mostrara un mensaje de error. ´´´

- [Volver al indice](#secciones)

#### Eventos

En esta pantalla podemos crear y administrar los XXX

##### Crear / Editar XXX

La pantalla de creación de XXX y de edición son la misma, la diferencia es que en la edición trae los datos del XXX que queremos modificar.

En esta pantalla podremos:

##### Eliminar XXX

Para eliminar un XXX se selecciona este tildándolo y en el menu de acciones seleccionar la opción *"Eliminar XXX seleccionados/as"* , luego presionar el botón Ejecutar.

Si esta todo correcto se pedirá la confirmación de la eliminación.

Luego de aceptar volveremos al listado y veremos la confirmación del borrado.

Si llega a haber un XXX el XXX asociado nos mostrara un mensaje de error.

- [Volver al indice](#secciones)

#### Accounts

En esta pantalla podemos crear y administrar los XXX

##### Crear / Editar XXX

La pantalla de creación de XXX y de edición son la misma, la diferencia es que en la edición trae los datos del XXX que queremos modificar.

En esta pantalla podremos:

##### Eliminar XXX

Para eliminar un XXX se selecciona este tildándolo y en el menu de acciones seleccionar la opción *"Eliminar XXX seleccionados/as"* , luego presionar el botón Ejecutar.

Si esta todo correcto se pedirá la confirmación de la eliminación.

Luego de aceptar volveremos al listado y veremos la confirmación del borrado.

Si llega a haber un XXX el XXX asociado nos mostrara un mensaje de error.

- [Volver al indice](#secciones)

#### Clientes

En esta pantalla podemos crear y administrar los XXX

##### Crear / Editar XXX

La pantalla de creación de XXX y de edición son la misma, la diferencia es que en la edición trae los datos del XXX que queremos modificar.

En esta pantalla podremos:

##### Eliminar XXX

Para eliminar un XXX se selecciona este tildándolo y en el menu de acciones seleccionar la opción *"Eliminar XXX seleccionados/as"* , luego presionar el botón Ejecutar.

Si esta todo correcto se pedirá la confirmación de la eliminación.

Luego de aceptar volveremos al listado y veremos la confirmación del borrado.

Si llega a haber un XXX el XXX asociado nos mostrara un mensaje de error.

- [Volver al indice](#secciones)

#### Clientes addresss

En esta pantalla podemos crear y administrar los XXX

##### Crear / Editar XXX

La pantalla de creación de XXX y de edición son la misma, la diferencia es que en la edición trae los datos del XXX que queremos modificar.

En esta pantalla podremos:

##### Eliminar XXX

Para eliminar un XXX se selecciona este tildándolo y en el menu de acciones seleccionar la opción *"Eliminar XXX seleccionados/as"* , luego presionar el botón Ejecutar.

Si esta todo correcto se pedirá la confirmación de la eliminación.

Luego de aceptar volveremos al listado y veremos la confirmación del borrado.

Si llega a haber un XXX el XXX asociado nos mostrara un mensaje de error.

- [Volver al indice](#secciones)

#### Clientes contacts

En esta pantalla podemos crear y administrar los XXX

##### Crear / Editar XXX

La pantalla de creación de XXX y de edición son la misma, la diferencia es que en la edición trae los datos del XXX que queremos modificar.

En esta pantalla podremos:

##### Eliminar XXX

Para eliminar un XXX se selecciona este tildándolo y en el menu de acciones seleccionar la opción *"Eliminar XXX seleccionados/as"* , luego presionar el botón Ejecutar.

Si esta todo correcto se pedirá la confirmación de la eliminación.

Luego de aceptar volveremos al listado y veremos la confirmación del borrado.

Si llega a haber un XXX el XXX asociado nos mostrara un mensaje de error.

- [Volver al indice](#secciones)

#### Clientes emails

En esta pantalla podemos crear y administrar los XXX

##### Crear / Editar XXX

La pantalla de creación de XXX y de edición son la misma, la diferencia es que en la edición trae los datos del XXX que queremos modificar.

En esta pantalla podremos:

##### Eliminar XXX

Para eliminar un XXX se selecciona este tildándolo y en el menu de acciones seleccionar la opción *"Eliminar XXX seleccionados/as"* , luego presionar el botón Ejecutar.

Si esta todo correcto se pedirá la confirmación de la eliminación.

Luego de aceptar volveremos al listado y veremos la confirmación del borrado.

Si llega a haber un XXX el XXX asociado nos mostrara un mensaje de error.

- [Volver al indice](#secciones)

#### Clientes socials

En esta pantalla podemos crear y administrar los XXX

##### Crear / Editar XXX

La pantalla de creación de XXX y de edición son la misma, la diferencia es que en la edición trae los datos del XXX que queremos modificar.

En esta pantalla podremos:

##### Eliminar XXX

Para eliminar un XXX se selecciona este tildándolo y en el menu de acciones seleccionar la opción *"Eliminar XXX seleccionados/as"* , luego presionar el botón Ejecutar.

Si esta todo correcto se pedirá la confirmación de la eliminación.

Luego de aceptar volveremos al listado y veremos la confirmación del borrado.

Si llega a haber un XXX el XXX asociado nos mostrara un mensaje de error.

- [Volver al indice](#secciones)

#### Clientes utms

En esta pantalla podemos crear y administrar los XXX

##### Crear / Editar XXX

La pantalla de creación de XXX y de edición son la misma, la diferencia es que en la edición trae los datos del XXX que queremos modificar.

En esta pantalla podremos:

##### Eliminar XXX

Para eliminar un XXX se selecciona este tildándolo y en el menu de acciones seleccionar la opción *"Eliminar XXX seleccionados/as"* , luego presionar el botón Ejecutar.

Si esta todo correcto se pedirá la confirmación de la eliminación.

Luego de aceptar volveremos al listado y veremos la confirmación del borrado.

Si llega a haber un XXX el XXX asociado nos mostrara un mensaje de error.

- [Volver al indice](#secciones)

#### Clientes webs

En esta pantalla podemos crear y administrar los XXX

##### Crear / Editar XXX

La pantalla de creación de XXX y de edición son la misma, la diferencia es que en la edición trae los datos del XXX que queremos modificar.

En esta pantalla podremos:

##### Eliminar XXX

Para eliminar un XXX se selecciona este tildándolo y en el menu de acciones seleccionar la opción *"Eliminar XXX seleccionados/as"* , luego presionar el botón Ejecutar.

Si esta todo correcto se pedirá la confirmación de la eliminación.

Luego de aceptar volveremos al listado y veremos la confirmación del borrado.

Si llega a haber un XXX el XXX asociado nos mostrara un mensaje de error.

- [Volver al indice](#secciones)

#### Contact types

En esta pantalla podemos crear y administrar los XXX

##### Crear / Editar XXX

La pantalla de creación de XXX y de edición son la misma, la diferencia es que en la edición trae los datos del XXX que queremos modificar.

En esta pantalla podremos:

##### Eliminar XXX

Para eliminar un XXX se selecciona este tildándolo y en el menu de acciones seleccionar la opción *"Eliminar XXX seleccionados/as"* , luego presionar el botón Ejecutar.

Si esta todo correcto se pedirá la confirmación de la eliminación.

Luego de aceptar volveremos al listado y veremos la confirmación del borrado.

Si llega a haber un XXX el XXX asociado nos mostrara un mensaje de error.

- [Volver al indice](#secciones)

#### Countryss

En esta pantalla podemos crear y administrar los XXX

##### Crear / Editar XXX

La pantalla de creación de XXX y de edición son la misma, la diferencia es que en la edición trae los datos del XXX que queremos modificar.

En esta pantalla podremos:

##### Eliminar XXX

Para eliminar un XXX se selecciona este tildándolo y en el menu de acciones seleccionar la opción *"Eliminar XXX seleccionados/as"* , luego presionar el botón Ejecutar.

Si esta todo correcto se pedirá la confirmación de la eliminación.

Luego de aceptar volveremos al listado y veremos la confirmación del borrado.

Si llega a haber un XXX el XXX asociado nos mostrara un mensaje de error.

- [Volver al indice](#secciones)

#### Email types

En esta pantalla podemos crear y administrar los XXX

##### Crear / Editar XXX

La pantalla de creación de XXX y de edición son la misma, la diferencia es que en la edición trae los datos del XXX que queremos modificar.

En esta pantalla podremos:

##### Eliminar XXX

Para eliminar un XXX se selecciona este tildándolo y en el menu de acciones seleccionar la opción *"Eliminar XXX seleccionados/as"* , luego presionar el botón Ejecutar.

Si esta todo correcto se pedirá la confirmación de la eliminación.

Luego de aceptar volveremos al listado y veremos la confirmación del borrado.

Si llega a haber un XXX el XXX asociado nos mostrara un mensaje de error.

- [Volver al indice](#secciones)

#### Excel filess

En esta pantalla podemos crear y administrar los XXX

##### Crear / Editar XXX

La pantalla de creación de XXX y de edición son la misma, la diferencia es que en la edición trae los datos del XXX que queremos modificar.

En esta pantalla podremos:

##### Eliminar XXX

Para eliminar un XXX se selecciona este tildándolo y en el menu de acciones seleccionar la opción *"Eliminar XXX seleccionados/as"* , luego presionar el botón Ejecutar.

Si esta todo correcto se pedirá la confirmación de la eliminación.

Luego de aceptar volveremos al listado y veremos la confirmación del borrado.

Si llega a haber un XXX el XXX asociado nos mostrara un mensaje de error.

- [Volver al indice](#secciones)

#### Mail corps

En esta pantalla podemos crear y administrar los XXX

##### Crear / Editar XXX

La pantalla de creación de XXX y de edición son la misma, la diferencia es que en la edición trae los datos del XXX que queremos modificar.

En esta pantalla podremos:

##### Eliminar XXX

Para eliminar un XXX se selecciona este tildándolo y en el menu de acciones seleccionar la opción *"Eliminar XXX seleccionados/as"* , luego presionar el botón Ejecutar.

Si esta todo correcto se pedirá la confirmación de la eliminación.

Luego de aceptar volveremos al listado y veremos la confirmación del borrado.

Si llega a haber un XXX el XXX asociado nos mostrara un mensaje de error.

- [Volver al indice](#secciones)

#### Mails

En esta pantalla podemos crear y administrar los mails que luego se enviaran a los clientes.

[![Listar Mails Vacío](img\10_mails_list_empty.png "Listar Mails Vacío")](img\10_mails_list_empty.png "Listar Mails Vacío")

Al ingresar en esta sección tenemos un listado de los mails ya creados. Estos tienen un reborde de color diferente dependiendo del tiempo faltante para el envío del proximo mail.

[![Listar Mails](img\10_mails_list.png "Listar Mails")](img\10_mails_list.png "Listar Mails")

En esta pantalla podemos ordenar los mails por los items del titulo, simplemente haciendo click sobre el nombre en el titulo. (Por Ejemplo: si queremos ordenar los mails por el estado, hacemos click sobre el titulo que dice STATUS).

[![Ordenar Mails](img\10_mails_ordenar.png "Ordenar Mails")](img\10_mails_ordenar.png "Ordenar Mails")

Podemos ademas filtrar los elementos de la lista por la casilla desde la que se van a enviar, por el numero de envío o por el estado. Esto lo logramos presionando en las opciones dentro del cuadro de filtrar.

[![Filtrar Mails](img\10_mails_filtrar.png "Filtrar Mails")](img\10_mails_filtrar.png "Filtrar Mails")

Dentro de las acciones generales que podemos tomar en esta pantalla se encuentran: Editar los datos del mail, accediendo a su información haciendo click sobre el nombre del mail corporativo asociado (dato azul del listado).

[![Botón editar Mail](img\10_mails_boton_editar.png "Botón editar Mail")](img\10_mails_boton_editar.png "Botón editar Mail")

Crear uno nuevo presionando en el botón agregar.

[![Botón crear Mail](img\10_mails_boton_crear.png "Botón crear Mail")](img\10_mails_boton_crear.png "Botón crear Mail")

O eliminar el mail, tildándolo, seleccionando la acción "Eliminar mails seleccionados/as" y presionando en ejecutar.

##### Crear / Editar Mails

La pantalla de creación de Mail y de edición son la misma, la diferencia es que en la edición trae los datos del mail que queremos modificar.

[![Editar Mail](img\10_mails_editar.png "Editar Mail")](img\10_mails_editar.png "Editar Mail")

En esta pantalla podremos:

- Seleccionar la casilla desde la que se va a enviar el mail. 
- Seleccionar el cliente.
- Poner un Subject al mail.
- Escribir un cuerpo personalizado para el mail. Este cuerpo puede contener texto enriquecido e imágenes.
- Agregar archivos adjuntos al mail.
- Tildar el mail como activo.
- Tildar el mail como respondido.
- Tildar el mail como que tiene un template asociado para utilizar.
- Se puede seleccionar el grupo de templates que tiene asociado.
- Modificar el numero de mail enviado
- Modificar cuando se envío el ultimo mail.
- Cambiar la frecuencia a la que debe enviarse los mails.

##### Eliminar Mails

Para eliminar un mail se selecciona este tildándolo y en el menu de acciones seleccionar la opción *"Eliminar mails seleccionados/as"* , luego presionar el botón Ejecutar.

[![Eliminar Mail](img\10_mails_eliminar.png "Eliminar Mail")](img\10_mails_eliminar.png "Editar Mail")

Si esta todo correcto se pedirá la confirmación de la eliminación.

[![Confirmar Eliminar Mail](img\10_mails_eliminar_confirmacion.png "Confirmar Eliminar Mail")](img\10_mails_eliminar_confirmacion.png "Confirmar Editar Mail")

Luego de aceptar volveremos al listado y veremos la confirmación del borrado.

[![Eliminar Mail Correcto](img\10_mails_eliminar_correcto.png "Confirmar Eliminar Correcto")](img\10_mails_eliminar_correcto.png "Editar Mail Correcto")

Si llega a haber un mail en la cola de envío asociado nos mostrara un mensaje de error.

[![Eliminar Mail error](img\10_mails_eliminar_error.png "Eliminar Mail error")](img\10_mails_eliminar_error.png "Editar Mail")

##### Preparar Envío

Para preparar el envío de los mails vamos a seleccionarlos y en el selector de acciones vamos a poner la opción *"Preparar envío"*.

[![Preparar envío](img\10_mails_preparar_envio.png "Preparar envío")](img\10_mails_preparar_envio.png "Preparar envío")

Una vez preparado el envio se creara un registro en Mails to send.

- [Volver al indice](#secciones)

#### Mails to sends

En esta pantalla podemos editar y administrar la cola de envío de mails.

##### Editar Mails to send

La pantalla de creación de XXX y de edición son la misma, la diferencia es que en la edición trae los datos del XXX que queremos modificar.

En esta pantalla podremos:

##### Eliminar XXX

Para eliminar un XXX se selecciona este tildándolo y en el menu de acciones seleccionar la opción *"Eliminar XXX seleccionados/as"* , luego presionar el botón Ejecutar.

Si esta todo correcto se pedirá la confirmación de la eliminación.

Luego de aceptar volveremos al listado y veremos la confirmación del borrado.

Si llega a haber un XXX el XXX asociado nos mostrara un mensaje de error.

- [Volver al indice](#secciones)

#### Social types

En esta pantalla podemos crear y administrar los XXX

##### Crear / Editar XXX

La pantalla de creación de XXX y de edición son la misma, la diferencia es que en la edición trae los datos del XXX que queremos modificar.

En esta pantalla podremos:

##### Eliminar XXX

Para eliminar un XXX se selecciona este tildándolo y en el menu de acciones seleccionar la opción *"Eliminar XXX seleccionados/as"* , luego presionar el botón Ejecutar.

Si esta todo correcto se pedirá la confirmación de la eliminación.

Luego de aceptar volveremos al listado y veremos la confirmación del borrado.

Si llega a haber un XXX el XXX asociado nos mostrara un mensaje de error.

- [Volver al indice](#secciones)

#### Template filess

En esta pantalla podemos crear y administrar los XXX

##### Crear / Editar XXX

La pantalla de creación de XXX y de edición son la misma, la diferencia es que en la edición trae los datos del XXX que queremos modificar.

En esta pantalla podremos:

##### Eliminar XXX

Para eliminar un XXX se selecciona este tildándolo y en el menu de acciones seleccionar la opción *"Eliminar XXX seleccionados/as"* , luego presionar el botón Ejecutar.

Si esta todo correcto se pedirá la confirmación de la eliminación.

Luego de aceptar volveremos al listado y veremos la confirmación del borrado.

Si llega a haber un XXX el XXX asociado nos mostrara un mensaje de error.

- [Volver al indice](#secciones)

#### Templates groups

En esta pantalla podemos crear y administrar los XXX

##### Crear / Editar XXX

La pantalla de creación de XXX y de edición son la misma, la diferencia es que en la edición trae los datos del XXX que queremos modificar.

En esta pantalla podremos:

##### Eliminar XXX

Para eliminar un XXX se selecciona este tildándolo y en el menu de acciones seleccionar la opción *"Eliminar XXX seleccionados/as"* , luego presionar el botón Ejecutar.

Si esta todo correcto se pedirá la confirmación de la eliminación.

Luego de aceptar volveremos al listado y veremos la confirmación del borrado.

Si llega a haber un XXX el XXX asociado nos mostrara un mensaje de error.

- [Volver al indice](#secciones)

#### Web types

En esta pantalla podemos crear y administrar los XXX

##### Crear / Editar Web types

La pantalla de creación de Web types y de edición son la misma, la diferencia es que en la edición trae los datos del Web types que queremos modificar.

En esta pantalla podremos:

##### Eliminar Web types

Para eliminar un Web types se selecciona este tildándolo y en el menu de acciones seleccionar la opción *"Eliminar Web types seleccionados/as"* , luego presionar el botón Ejecutar.

Si esta todo correcto se pedirá la confirmación de la eliminación.

Luego de aceptar volveremos al listado y veremos la confirmación del borrado.

Si llega a haber un Web types asociado a algún registro nos mostrara un mensaje de error.

- [Volver al indice](#secciones)

### Calendario

[![Calendario](img\12_calendario.png "Calendario")](img\12_calendario.png "Calendario")

[![Listado de eventos](img\12_calendario_listado_eventos.png "Listado de eventos")](img\12_calendario_listado_eventos.png "Listado de eventos")

## Notas importantes

Es muy importante crear las [cuentas](#accounts) y los [mails corporativos](#mail-corps) asociados antes de procesar el Excel. De otra forma es muy probable que se retorne un mensaje de error.

[![Error al importar](img\05_excel_error.png "Error al importar")](img\05_excel_error.png "Error al importar")